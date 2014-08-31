# encoding: utf-8


class StateMachine(object):
    def __init__(self, entity):
        self.entity = entity
        self.current_state = None
        self.global_state = None
        self.previous_state = None

    def handle_message(self, sender, receiver, msg):
        if self.current_state and self.current_state.on_message(sender, self.entity, msg):
            return True
        if self.global_state and self.global_state.on_message(sender, self.entity, msg):
            return True
        return False

    def set_current_state(self, state):
        self.current_state = state

    def set_global_state(self, state):
        self.global_state = state

    def set_previous_state(self, state):
        self.previous_state = state

    def update(self):
        if self.global_state is not None:
            self.global_state.update(self.entity)
        if self.current_state is not None:
            self.current_state.update(self.entity)

    def change_state(self, state):
        if self.current_state is not None:
            self.set_previous_state(self.current_state)
            self.current_state.exit(self.entity)
        self.set_current_state(state)
        self.current_state.enter(self.entity)

    def revert_to_previous_state(self):
        if self.previous_state is not None:
            self.change_state(self.previous_state)

    def is_in_state(self, state):
        self.current_state == state
