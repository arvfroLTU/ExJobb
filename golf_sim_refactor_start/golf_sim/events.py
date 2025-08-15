from collections import defaultdict
from typing import Callable, Any

class EventBus:
    def __init__(self):
        self._listeners: dict[str, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event_type: str, listener: Callable[[Any], None]) -> None:
        self._listeners[event_type].append(listener)

    def publish(self, event_type: str, data: Any) -> None:
        for fn in list(self._listeners.get(event_type, [])):
            fn(data)
