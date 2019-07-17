"""Shows example react handling for state changes.

A handler may die suddenly without warning due to any number of reasons,
in which case Juju will attempt to run the handler again with the same
arguments, until it gets a `ChangeApproved` or `ChangeHandled` response.
This may result in the function having to handle a partial state change,
in which case the handler may log a warning and update state anyways, or
just deny the change and tell an administrator that they have to straighten
things out.
"""


# Classes in charm.state.reactions or somesuch
class StateReaction:
    pass


class ChangeApproved(StateReaction):
    """Signifies that the charm code approved the state change.

    The code didn't handle the change itself though, and Juju should
    proceed with default state change update handling.
    """


class ChangeHandled(StateReaction):
    """Signifies that the charm code approved and updated the state."""


class ChangeDenied(StateReaction):
    """Signifies that the charm code denied updating the state."""
    def __init__(self, reason: str):
        self.reason = reason


# Classes in charm.state or somesuch
class State:
    def __init__(self):
        self.config = {}
        self.relations = {}
        self.juju = {}


class Diff:
    def __init__(self):
        self.config = {}
        self.relations = {}
        self.juju = {}


# Noop handler, returning `None` means proceed with default behavior
# Should probably emit a warning and prefer an explicit approval, though
def react_noop(new_state: State, old_state: State, diff: Diff) -> StateReaction:
    ...


# Example handler showing an exception being thrown. Equivalent to
# try:
#     handle_change()
# except Exception as err:
#     return ChangeDenied(str(err))
def react_error(new_state: State, old_state: State, diff: Diff) -> StateReaction:
    raise Exception("Something happened!")


# Example handler that always denies a state change
def react_deny(new_state: State, old_state: State, diff: Diff) -> StateReaction:
    return ChangeDenied('I don\'t like that change very much.')


# Example handler that always approves a state change
def react_approve(new_state: State, old_state: State, diff: Diff) -> StateReaction:
    return ChangeApproved()


# Example handler that checks something about the new state, and denies
# the change request if it finds something it doesn't like. The plain
# strings below would be passed to a SQL library IRL.
def react_check(new_state: State, old_state: State, diff: Diff) -> StateReaction:
    if new_state.config['user'] == 'root':
        return ChangeDenied('Non-root user can\'t be set to root!')

    if old_state.config['user']:
        existing_user = f"SELECT * FROM users WHERE name = {old_state.config['user']}"
        if not existing_user:
            print("WARN: Old user doesn't exist!")

    f"UPDATE users SET name = {new_state.config['user']} WHERE name = {old_state.config['user']}"

    return ChangeHandled()
