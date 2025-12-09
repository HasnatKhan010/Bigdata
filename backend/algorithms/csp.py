from typing import Any, Dict, List


def run_csp(drivers: List[Any], orders: List[Any]) -> Dict[str, Any]:
    # Placeholder for CSP-based assignment.
    assignments = {order.id: (drivers[0].id if drivers else None) for order in orders}
    return {"assignments": assignments, "algorithm": "CSP"}
