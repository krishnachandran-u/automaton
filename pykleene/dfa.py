class DFA:
    state: set[str]
    alphabet: set[str]
    transitions: dict[tuple[str, str], str]
    startState: str
    finalStates: set[str]