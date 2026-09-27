from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging

from app.services.telemetry_service import telemetry_service

router = APIRouter(prefix="/logs", tags=["Logs & Telemetry"])
logger = logging.getLogger("frontend_logger")

class LogMessage(BaseModel):
    level: str
    message: str
    timestamp: str
    source: str

class SpanLogRequest(BaseModel):
    trace_id: Optional[str] = None
    node_name: str
    duration_ms: float
    ttft_ms: Optional[float] = None
    status: str = "SUCCESS"
    error: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None

@router.post("/", status_code=201)
async def receive_log(log_msg: LogMessage, deviceId: Optional[str] = Query(None, description="Device ID")):
    formatted_msg = f"[FRONTEND - {log_msg.source}] {log_msg.timestamp} | {log_msg.message}"
    if log_msg.level.lower() == "error":
        logger.error(formatted_msg)
    elif log_msg.level.lower() == "warn":
        logger.warning(formatted_msg)
    elif log_msg.level.lower() == "debug":
        logger.debug(formatted_msg)
    else:
        logger.info(formatted_msg)
    
    # Record frontend log event in telemetry
    telemetry_service.record_span(
        trace_id=f"device_{deviceId or 'unknown'}",
        node_name=f"frontend_{log_msg.source}",
        duration_ms=0.0,
        status="ERROR" if log_msg.level.lower() == "error" else "SUCCESS",
        error=log_msg.message if log_msg.level.lower() == "error" else None,
        meta={"level": log_msg.level, "source": log_msg.source, "device_id": deviceId},
        metrics={"message_len": len(log_msg.message)}
    )
    
    return {"status": "success"}

@router.post("/span", status_code=201)
async def record_telemetry_span(span_req: SpanLogRequest):
    trace_id = span_req.trace_id or telemetry_service.generate_trace_id()
    telemetry_service.record_span(
        trace_id=trace_id,
        node_name=span_req.node_name,
        duration_ms=span_req.duration_ms,
        ttft_ms=span_req.ttft_ms,
        status=span_req.status,
        error=span_req.error,
        metrics=span_req.metrics,
        meta=span_req.meta
    )
    return {"status": "success", "trace_id": trace_id}

@router.get("/telemetry")
async def get_recent_telemetry_logs(
    limit: int = Query(50, ge=1, le=500),
    node_name: Optional[str] = Query(None, description="Filter by node name")
):
    logs = telemetry_service.get_recent_telemetry(limit=limit, node_name=node_name)
    return {"count": len(logs), "logs": logs}

@router.get("/summary")
async def get_telemetry_summary():
    summary = telemetry_service.get_node_performance_summary()
    return summary
