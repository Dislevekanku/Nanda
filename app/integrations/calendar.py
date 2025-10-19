"""Calendar integration stub."""

from datetime import datetime, timedelta
from typing import Any, Dict, List


def search_availability(provider_id: int | None = None) -> List[Dict[str, Any]]:
    """Return fake availability slots."""

    base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    return [
        {"provider_id": provider_id or 1, "start_time": (base_time + timedelta(days=1, hours=offset)).isoformat()}
        for offset in range(9, 15, 2)
    ]
