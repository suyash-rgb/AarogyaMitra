import os
import time
import json
import uuid
import threading
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class TelemetrySpan:
    def __init__(self, telemetry_service: 'TelemetryService', node_name: str, trace_id: Optional[str] = None, meta: Optional[Dict[str, Any]] = None):
        self.telemetry = telemetry_service
        self.node_name = node_name
        self.trace_id = trace_id or telemetry_service.generate_trace_id()
        self.meta = meta or {}
        self.metrics: Dict[str, Any] = {}
        self.ttft_ms: Optional[float] = None
        self.status = "SUCCESS"
        self.error: Optional[str] = None
        self.start_perf = 0.0
        self.start_time = 0.0

    def set_metric(self, key: str, value: Any):
        self.metrics[key] = value

    def set_meta(self, key: str, value: Any):
        self.meta[key] = value

    def set_ttft(self, ttft_ms: float):
        self.ttft_ms = round(float(ttft_ms), 2)

    def record_error(self, err: Any):
        self.status = "ERROR"
        self.error = str(err)

    def __enter__(self):
        self.start_perf = time.perf_counter()
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = round((time.perf_counter() - self.start_perf) * 1000, 2)
        if exc_val is not None:
            self.status = "ERROR"
            self.error = str(exc_val)

        start_iso = datetime.utcnow().isoformat() + "Z"

        self.telemetry.record_span(
            trace_id=self.trace_id,
            node_name=self.node_name,
            duration_ms=duration_ms,
            ttft_ms=self.ttft_ms,
            status=self.status,
            error=self.error,
            metrics=self.metrics,
            meta=self.meta,
            timestamp=start_iso
        )


class TelemetryService:
    _instance: Optional['TelemetryService'] = None
    _lock = threading.Lock()

    def __init__(self, log_dir: Optional[str] = None):
        if log_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            log_dir = os.path.join(base_dir, "logs")
        
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.jsonl_path = os.path.join(self.log_dir, "pipeline_telemetry.jsonl")
        self.md_path = os.path.join(self.log_dir, "pipeline_telemetry.md")
        self._ensure_md_header()

    def _ensure_md_header(self):
        if not os.path.exists(self.md_path):
            try:
                with open(self.md_path, "w", encoding="utf-8") as f:
                    f.write("# AarogyaMitra Pipeline Telemetry Log\n\n")
                    f.write("| Timestamp | Trace ID | Node | Latency (ms) | TTFT (ms) | Status | Key Metrics | Meta |\n")
                    f.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")
            except Exception as e:
                logger.error(f"Failed to write telemetry header: {e}")

    @classmethod
    def get_instance(cls, log_dir: Optional[str] = None) -> 'TelemetryService':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = TelemetryService(log_dir=log_dir)
        return cls._instance

    def generate_trace_id(self) -> str:
        return f"trace_{uuid.uuid4().hex[:12]}"

    def span(self, node_name: str, trace_id: Optional[str] = None, meta: Optional[Dict[str, Any]] = None) -> TelemetrySpan:
        return TelemetrySpan(self, node_name=node_name, trace_id=trace_id, meta=meta)

    def record_span(
        self,
        trace_id: str,
        node_name: str,
        duration_ms: float,
        ttft_ms: Optional[float] = None,
        status: str = "SUCCESS",
        error: Optional[str] = None,
        metrics: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None
    ):
        ts = timestamp or (datetime.utcnow().isoformat() + "Z")
        metrics_dict = metrics or {}
        meta_dict = meta or {}

        entry = {
            "timestamp": ts,
            "trace_id": trace_id,
            "node_name": node_name,
            "duration_ms": duration_ms,
            "ttft_ms": ttft_ms,
            "status": status,
            "error": error,
            "metrics": metrics_dict,
            "meta": meta_dict
        }

        with self._lock:
            try:
                with open(self.jsonl_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry) + "\n")
            except Exception as e:
                logger.error(f"Error writing JSONL telemetry: {e}")

            try:
                metrics_str = json.dumps(metrics_dict) if metrics_dict else "-"
                meta_str = json.dumps(meta_dict) if meta_dict else "-"
                ttft_str = f"{ttft_ms:.1f}" if ttft_ms is not None else "N/A"
                
                with open(self.md_path, "a", encoding="utf-8") as f:
                    f.write(f"| {ts} | `{trace_id}` | `{node_name}` | {duration_ms:.2f} | {ttft_str} | {status} | `{metrics_str}` | `{meta_str}` |\n")
            except Exception as e:
                logger.error(f"Error writing MD telemetry: {e}")

    def get_recent_telemetry(self, limit: int = 50, node_name: Optional[str] = None) -> List[Dict[str, Any]]:
        if not os.path.exists(self.jsonl_path):
            return []
        
        results = []
        try:
            with open(self.jsonl_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    if node_name and data.get("node_name") != node_name:
                        continue
                    results.append(data)
                    if len(results) >= limit:
                        break
        except Exception as e:
            logger.error(f"Error reading telemetry log: {e}")
        
        return results

    def get_node_performance_summary(self) -> Dict[str, Any]:
        if not os.path.exists(self.jsonl_path):
            return {"total_spans": 0, "nodes": {}}

        nodes: Dict[str, List[Dict[str, Any]]] = {}
        total_spans = 0

        try:
            with open(self.jsonl_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    node = data.get("node_name", "unknown")
                    if node not in nodes:
                        nodes[node] = []
                    nodes[node].append(data)
                    total_spans += 1
        except Exception as e:
            logger.error(f"Error parsing telemetry for summary: {e}")

        summary_by_node = {}
        for node, span_list in nodes.items():
            durations = [s["duration_ms"] for s in span_list if "duration_ms" in s]
            ttfts = [s["ttft_ms"] for s in span_list if s.get("ttft_ms") is not None]
            errors = sum(1 for s in span_list if s.get("status") == "ERROR")
            
            avg_duration = round(sum(durations) / len(durations), 2) if durations else 0.0
            p95_index = int(len(durations) * 0.95)
            p95_duration = round(sorted(durations)[min(p95_index, len(durations)-1)], 2) if durations else 0.0
            avg_ttft = round(sum(ttfts) / len(ttfts), 2) if ttfts else None

            summary_by_node[node] = {
                "count": len(span_list),
                "avg_duration_ms": avg_duration,
                "p95_duration_ms": p95_duration,
                "min_duration_ms": round(min(durations), 2) if durations else 0.0,
                "max_duration_ms": round(max(durations), 2) if durations else 0.0,
                "avg_ttft_ms": avg_ttft,
                "error_count": errors,
                "error_rate": round(errors / len(span_list), 4) if span_list else 0.0
            }

        return {
            "total_spans": total_spans,
            "nodes": summary_by_node
        }

telemetry_service = TelemetryService.get_instance()
