import graphviz
class DFA:
    states: set[str]
    alphabet: set[str]
    transitions: dict[tuple[str, str], str]
    startState: str
    finalStates: set[str]

    def __init__(self, 
                 states: set[str] = set(), 
                 alphabet: set[str] = set(), 
                 transitions: dict[tuple[str, str], str] = dict(), 
                 startState: str = None, 
                 finalStates: set[str] = set()):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.startState = startState
        self.finalStates = finalStates

    def loadFromJSONDict(self, data: dict):
        try:
            dfa = DFA()
            dfa.states = set(data['states'])
            dfa.alphabet = set(data['alphabet'])
            dfa.transitions = {tuple(transition[:2]): transition[2] for transition in data["transitions"]} 
            dfa.startState = data['startState']
            dfa.finalStates = set(data['finalStates'])

            if dfa.isValid():
                self.states = dfa.states
                self.alphabet = dfa.alphabet
                self.transitions = dfa.transitions
                self.startState = dfa.startState
                self.finalStates = dfa.finalStates
            else:
                raise Exception("Invalid DFA")
        except Exception as e:
            print(f"Error while loading DFA from JSON: {e}")

    def isValid(self) -> bool:
        if self.startState not in self.states:
            return False
        if not self.finalStates.issubset(self.states):
            return False
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.transitions:
                    return False
                if self.transitions[(state, symbol)] not in self.states:
                    return False
        if len(self.transitions) != len(self.states) * len(self.alphabet):
            return False
        return True

    def __str__(self):
        states = ", ".join(self.states)
        alphabet = ", ".join(self.alphabet)
        transitions = "\n".join([f"δ({q}, {a}) = {self.transitions[(q, a)]}" for (q, a) in self.transitions.items()])
        startState = self.startState
        finalStates = ", ".join(self.finalStates)
        
        return f"Q = {{{states}}}\n\nΣ = {{{alphabet}}}\n\n{{{transitions}}}\n\ns = {startState}\n\nF = {{{finalStates}}}"

    def accepts(self, string: str = None, verbose: str = False) -> bool:
        currentState = self.startState
        for symbol in string:
            currentState = self.transitions[(currentState, symbol)]
            print(f"({currentState}, {symbol}) -> {self.transitions[(currentState, symbol)]}") if verbose else None
        return currentState in self.finalStates

    def nextState(self, currentState: str, symbol: str) -> str:
        if (currentState, symbol) in self.transitions:
            return self.transitions[(currentState, symbol)]
        else:
            return None

    def minimal(self) -> 'DFA':
        from pykleene.utils import getAllStrings
        import copy

        dfaCopy = copy.deepcopy(self)

        states = list(dfaCopy.states)
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
            states=set(newStates),
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
    
        if len(minDfa1.states) != len(minDfa2.states):
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
                nextState1 = minDfa1.nextState(state1, symbol)
                nextState2 = minDfa2.nextState(state2, symbol)
    
                if areStatesNonEquivalent(nextState1, nextState2):
                    return False
    
                if (nextState1, nextState2) not in visited:
                    visited[(nextState1, nextState2)] = True
                    bfsQueue.append((nextState1, nextState2))
    
        return True
    
    def image(self, dir: str = None, save: bool = False) -> 'graphviz.Digraph':
        from pykleene._config import graphvizConfig 

        dot = graphviz.Digraph(**graphvizConfig)

        for state in self.states:
            if state in self.finalStates:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        dot.node(f'{id(self.startState)}', shape='point', label='')
        dot.edge(f'{id(self.startState)}', self.startState)

        for (state, symbol), nextState in self.transitions.items():
            dot.edge(state, nextState, label=symbol)

        if dir and save:
            try:
                dot.render(f"{dir}/<dfa>{id(self)}", format='png', cleanup=True)
            except Exception as e:
                print(f"Error while saving image: {e}")
        return dot

    def union(self, dfa: 'DFA') -> 'DFA':
        if self.alphabet != dfa.alphabet: 
            print("Alphabets of the DFAs do not match.")
            return None

        newStates = set((state1, state2) for state1 in self.states for state2 in dfa.states)
        newFinalStates = set((state1, state2) for state1 in self.finalStates for state2 in dfa.states) | set((state1, state2) for state1 in self.states for state2 in dfa.finalStates)
        newStartState = (self.startState, dfa.startState)
        newTransitions = set(
            ((state1, state2), symbol, (self.nextState(state1, symbol), dfa.nextState(state2, symbol))) 
            for state1, state2 in newStates 
            for symbol in self.alphabet
        )

        unionDfa = DFA(
            states = set(str(state) for state in newStates),
            alphabet = self.alphabet,
            transitions = {(str(state), symbol): str(nextState) for (state, symbol, nextState) in newTransitions},
            startState = str(newStartState),
            finalStates = set(str(state) for state in newFinalStates)
        )

        return unionDfa.reachable()

    def complement(self) -> 'DFA':
        complementDfa = DFA(
            states = self.states,
            alphabet = self.alphabet,
            transitions = self.transitions,
            startState = self.startState,
            finalStates = self.states - self.finalStates
        )

        return complementDfa

    def intersection(self, dfa: 'DFA') -> 'DFA':
        complementSelf = self.complement() 
        complementDfa = dfa.complement()
        unionDfa = complementSelf.union(complementDfa)
        complementUnionDfa = unionDfa.complement()

        return complementUnionDfa

    def reachable(self) -> 'DFA':
        reachableStates = set()
        reachableStates.add(self.startState)

        statesQueue = [self.startState]

        while statesQueue:
            state = statesQueue.pop(0)
            for symbol in self.alphabet:
                nextState = self.nextState(state, symbol)
                if nextState not in reachableStates:
                    reachableStates.add(nextState)
                    statesQueue.append(nextState)

        newFinalStates = self.finalStates & reachableStates
        newTransitions = {(state, symbol): nextState 
                          for (state, symbol), nextState in self.transitions.items() 
                          if state in reachableStates and nextState in reachableStates}

        reachableDfa = DFA(
            states = reachableStates,
            alphabet = self.alphabet,
            transitions = newTransitions,
            startState = self.startState,
            finalStates = newFinalStates
        )

        return reachableDfa

    def isLangSubset(self, dfa: 'DFA') -> bool:
        intersectionDfa = self.intersection(dfa)
        minimalIntersectionDfa = intersectionDfa.minimal()
        minSelf = self.minimal()
        return minSelf.isomorphic(minimalIntersectionDfa)

    def difference(self, dfa: 'DFA') -> 'DFA':
        return self.intersection(dfa.complement())

    def symmetricDifference(self, dfa: 'DFA') -> 'DFA':
        return self.union(dfa).difference(self.intersection(dfa))

