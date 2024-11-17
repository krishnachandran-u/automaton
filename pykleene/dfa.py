import copy
from utils import getAllStrings
class DFA:
    state: set[str]
    alphabet: set[str]
    transitions: dict[tuple[str, str], str]
    startState: str
    finalStates: set[str]

    def __init__(self, 
                 state: set[str] = set(), 
                 alphabet: set[str] = set(), 
                 transitions: dict[tuple[str, str], str] = dict(), 
                 startState: str = None, 
                 finalStates: set[str] = set()):
        self.state = state
        self.alphabet = alphabet
        self.transitions = transitions
        self.startState = startState
        self.finalStates = finalStates

    def __str__(self):
        states = ", ".join(self.state)
        alphabet = ", ".join(self.alphabet)
        transitions = "\n".join([f"δ({q}, {a}) = {self.transitions[(q, a)]}" for (q, a) in self.transitions.items()])
        startState = self.startState
        finalStates = ", ".join(self.finalStates)
        
        return f"Q = {{{states}}}\n\nΣ = {{{alphabet}}}\n\n{{{transitions}}}\n\ns = {startState}\n\nF = {{{finalStates}}}"

    def accepts(self, string: str) -> bool:
        currentState = self.startState
        for symbol in string:
            currentState = self.transitions[(currentState, symbol)]
        return currentState in self.finalStates

    def next_state(self, current_state: str, symbol: str) -> str:
        if (current_state, symbol) in self.transitions:
            return self.transitions[(current_state, symbol)]
        else:
            return None

    def minimal(self) -> 'DFA':
        dfaCopy = copy.deepcopy(self)

        states = list(dfaCopy.state)
        alphabet = list(dfaCopy.alphabet)
        transitions = dfaCopy.transitions
        finalStates = dfaCopy.finalStates
        startState = dfaCopy.startState

        grid = [[True for _ in range(len(states))] for _ in range(len(states))]
        equivalenceClasses: list[list[str]] = []

        strings = getAllStrings(alphabet, len(states) - 1)

        for i in range(len(states)):
            for j in range(i):
                dfa1 = copy.deepcopy(dfaCopy)
                dfa2 = copy.deepcopy(dfaCopy)
                dfa1.startState = states[i]
                dfa2.startState = states[j]

                for string in strings:
                    if dfa1.accepts(string) != dfa2.accepts(string):
                        grid[i][j] = False
                        break

        for i in range(len(states)):
            for j in range(i + 1):
                if grid[i][j]:
                    equivalenceClassFound = False
                    if i != j:
                        for equivalenceClass in equivalenceClasses:
                            if states[i] in equivalenceClass:
                                equivalenceClass.append(states[j])
                                equivalenceClassFound = True
                                break
                            elif states[j] in equivalenceClass:
                                equivalenceClass.append(states[i])
                                equivalenceClassFound = True
                                break
                        if not equivalenceClassFound:
                            equivalenceClasses.append([states[i], states[j]])
                    else:
                        for equivalenceClass in equivalenceClasses:
                            if states[i] in equivalenceClass:
                                equivalenceClassFound = True
                                break
                        if not equivalenceClassFound:
                            equivalenceClasses.append([states[i]])

        newTransitions = {}
        for (state, symbol), nextState in transitions.items():
            for equivalenceClass in equivalenceClasses:
                if state in equivalenceClass:
                    state = str(equivalenceClass)
                if nextState in equivalenceClass:
                    nextState = str(equivalenceClass)
            newTransitions[(state, symbol)] = nextState

        newStartState = None
        for equivalenceClass in equivalenceClasses:
            if startState in equivalenceClass:
                newStartState = str(equivalenceClass)
                break

        newFinalStates = set()
        for finalState in finalStates:
            for equivalenceClass in equivalenceClasses:
                if finalState in equivalenceClass:
                    newFinalStates.add(str(equivalenceClass))
                    break

        newStates = [str(equivalenceClass) for equivalenceClass in equivalenceClasses]

        newDfa = DFA(
            state=set(newStates),
            alphabet=set(alphabet),
            transitions=newTransitions,
            startState=newStartState,
            finalStates=newFinalStates
        )

        return newDfa

    def isomorphic(self, dfa: 'DFA') -> bool:
        minDfa1 = self.minimal()
        minDfa2 = dfa.minimal()

        if minDfa1.alphabet != minDfa2.alphabet:
            return False
        alphabet = list(minDfa1.alphabet)
    
        if len(minDfa1.state) != len(minDfa2.state):
            return False
    
        if (minDfa1.startState in minDfa1.finalStates) != (minDfa2.startState in minDfa2.finalStates):
            return False
    
        visited = {}
    
        bfsQueue = [(minDfa1.startState, minDfa2.startState)]
        visited[(minDfa1.startState, minDfa2.startState)] = True

        def areStatesNonEquivalent(state1: str, state2: str) -> bool:
            if (state1 in minDfa1.finalStates) != (state2 in minDfa2.finalStates):
                return True
            for visitedState1, visitedState2 in visited:
                if visitedState1 == state1 and visitedState2 != state2:
                    return True 
                if visitedState1 != state1 and visitedState2 == state2:
                    return True 
            return False
    
        while bfsQueue:
            state1, state2 = bfsQueue.pop(0)
    
            for symbol in alphabet:
                nextState1 = minDfa1.next_state(state1, symbol)
                nextState2 = minDfa2.next_state(state2, symbol)
    
                if areStatesNonEquivalent(nextState1, nextState2):
                    return False
    
                if (nextState1, nextState2) not in visited:
                    visited[(nextState1, nextState2)] = True
                    bfsQueue.append((nextState1, nextState2))
    
        return True
