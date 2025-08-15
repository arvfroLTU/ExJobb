class EventManager:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def dispatch(self, event_type, data=None):
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(data)


class PlayerStoppedEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Listener:
def on_player_stopped(event: PlayerStoppedEvent):
    print(f"Player died due to {event.reason} at {event.time}s")



def playerUpToBat(coords):
    print(f"Player is up to bat at coordinates: {coords}")
    return