from typing import Any, Dict, List


def run_csp(drivers: List[Any], orders: List[Any]) -> Dict[str, Any]:
    # Placeholder for CSP-based assignment with simple round-robin load spreading.
    def safe_id(entity: Any, fallback: str) -> str:
        entity_id = getattr(entity, "id", None)
        return str(entity_id) if entity_id is not None else fallback

    assignments: Dict[str, Any] = {}
    if not drivers:
        assignments = {safe_id(order, f"order_{idx}"): None for idx, order in enumerate(orders)}
    else:
        assignments = {
            safe_id(order, f"order_{idx}"): safe_id(drivers[idx % len(drivers)], f"driver_{idx}")
            for idx, order in enumerate(orders)
        }
    return {"assignments": assignments, "algorithm": "CSP"}
