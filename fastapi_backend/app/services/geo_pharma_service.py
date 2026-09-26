# services/geo_pharma_service.py / app/services/geo_pharma_service.py
import math
from typing import List, Dict, Optional, Any

class GeoPharmaService:
    def __init__(self, db_cursor=None):
        self.cursor = db_cursor

    def find_nearest_kendras(self, lat: float, lon: float, radius_km: float = 10.0, limit: int = 5) -> List[Dict]:
        """Finds stores within radius using PostGIS ST_DWithin and ST_Distance."""
        if not self.cursor:
            return []
        query = """
            SELECT kendra_id, kendra_name, address, pincode, district, state, phone,
                   ST_Distance(geom, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) / 1000.0 AS distance_km
            FROM jan_aushadhi_kendras
            WHERE ST_DWithin(geom, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s * 1000)
            ORDER BY distance_km ASC
            LIMIT %s;
        """
        self.cursor.execute(query, (lon, lat, lon, lat, radius_km, limit))
        return self.cursor.fetchall()

    def search_brand_substitute(self, query_name: str, limit: int = 3) -> List[Dict]:
        """Resolves trade brands to generic equivalents using trigram fuzzy matching."""
        if not self.cursor:
            return []
        query = """
            SELECT brand_name, generic_salt_name, dosage_form, brand_mrp, 
                   jan_aushadhi_mrp, savings_percentage,
                   similarity(brand_name, %s) AS match_score
            FROM medicine_master
            WHERE brand_name % %s OR generic_salt_name % %s
            ORDER BY match_score DESC
            LIMIT %s;
        """
        self.cursor.execute(query, (query_name, query_name, query_name, limit))
        return self.cursor.fetchall()

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Lightweight offline calculation fallback."""
        r = 6371.0
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2)**2
        return round(r * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))), 2)

geo_pharma_service = GeoPharmaService()
