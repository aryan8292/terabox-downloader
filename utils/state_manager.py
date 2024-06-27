
class StateManager:
    def __init__(self):
        self.user_states = {}

    def set_user_state(self, user_id, state):
        self.user_states[user_id] = state

    def get_user_state(self, user_id):
        return self.user_states.get(user_id, "level1")

_state_manager = StateManager()

def get_state_manager():
    return _state_manager