from datetime import datetime, timezone
from typing import Any


def check_database_connection() -> bool:
    """Check if the default database is reachable."""
    from django.db import connection

    try:
        connection.ensure_connection()
        return True
    except Exception:
        return False


def get_health_status(
    db_checker: Any = None,
    version: str = "1.0.0",
) -> dict:
    """Return health status as a dict.

    Args:
        db_checker: Callable returning bool for DB connectivity.
                    Defaults to check_database_connection.
        version: Application version string.

    Returns:
        Dict matching the HealthStatus schema.
    """
    if db_checker is None:
        db_checker = check_database_connection

    db_ok = db_checker()

    return {
        "status": "healthy" if db_ok else "unhealthy",
        "database": "connected" if db_ok else "disconnected",
        "version": version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
