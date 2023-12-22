
class SocketWrap:
    def __init__(self, socketio, event_name: str):
        self.event_name = event_name
        self.socketio = socketio
        self.enabled = False

    def on_event(self, func):
        if self.enabled:
            self.socketio.on(self.event_name)(func)

    def emit_data(self, data):
        if self.enabled:
            self.socketio.emit(self.event_name, data)

    def turn_on(self):
        self.enabled = True

    def turn_off(self):
        self.enabled = False
