class NFA:
    states: set[str]
    alphabet: set[str]
    transitions: dict[tuple[str, str], set[str]]
    startStates: set[str]
    finalStates: set[str]

    def __init__(self, 
                 states: set[str] = set(), 
                 alphabet: set[str] = set(), 
                 transitions: dict[tuple[str, str], set[str]] = dict(), 
                 startStates: set[str] = set(), 
                 finalStates: set[str] = set()):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.startStates = startStates
        self.finalStates = finalStates

    def loadFromJSONDict(self, data: dict):
        self.states = set(data['states'])
        self.alphabet = set(data['alphabet'])
        self.transitions = dict()
        for transition in data['transitions']:
            self.transitions[(transition[0], transition[1])] = set(transition[2])
        self.startStates = set(data['startStates'])
        self.finalStates = set(data['finalStates'])

    def singleStartStateNFA(self) -> 'NFA':
        from copy import deepcopy
        newNfa = deepcopy(self)
        cnt = 0
        while f"q{cnt}" in newNfa.states:
            cnt += 1
        newStartState = f"q{cnt}"
        newNfa.states.add(newStartState)
        for startState in newNfa.startStates:
            newNfa.transitions[(newStartState, 'ε')] = {startState}
        newNfa.startStates = {newStartState}
        return newNfa


    def singleFinalStateNFA(self) -> 'NFA':
        from copy import deepcopy
        newNfa = deepcopy(self)
        cnt = 0
        while f"q{cnt}" in newNfa.states:
            cnt += 1
        newFinalState = f"q{cnt}"
        newNfa.states.add(newFinalState)
        for finalState in newNfa.finalStates:
            newNfa.transitions[(finalState, 'ε')] = {newFinalState}
        newNfa.finalStates = {newFinalState}
        return newNfa 