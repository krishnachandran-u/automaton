from typing import TYPE_CHECKING
import graphviz

if TYPE_CHECKING:
    from pykleene.grammar import Grammar
    from pykleene.dfa import DFA
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

    def isValid(self) -> bool:
        for (state, symbol), nextStates in self.transitions.items():
            if state not in self.states:
                return False
            if symbol not in self.alphabet and symbol != 'ε':
                return False
            for nextState in nextStates:
                if nextState not in self.states:
                    return False
        if not self.startStates.issubset(self.states):
            return False
        if not self.finalStates.issubset(self.states):
            return False 
        return True

    def accepts(self, string: str = None) -> bool:
        def run(state: str, string: str) -> bool:
            if len(string) == 0:
                return state in self.finalStates
            for nextState in self.epsilonClosure(state):
                for nextNextState in self.nextStates(nextState, string[0]):
                    if run(nextNextState, string[1:]):
                        return True
            return False

        for startState in self.startStates:
            if run(startState, string):
                return True

        return False

    def loadFromJSONDict(self, data: dict):
        nfa = NFA()
        try:
            nfa.states = set(data['states'])
            nfa.alphabet = set(data['alphabet'])
            nfa.transitions = dict()
            for transition in data['transitions']:
                nfa.transitions[(transition[0], transition[1])] = set(transition[2])
            nfa.startStates = set(data['startStates'])
            nfa.finalStates = set(data['finalStates'])

            if nfa.isValid():
                self.states = nfa.states
                self.alphabet = nfa.alphabet
                self.transitions = nfa.transitions
                self.startStates = nfa.startStates
                self.finalStates = nfa.finalStates
            else:
                raise Exception("Invalid NFA")
        except Exception as e:
            print(f"Error while loading NFA from JSON dict: {e}")

    def addTransition(self, startState: str, symbol: str, endState: str) -> 'NFA':
        from copy import deepcopy
        nfa = deepcopy(self)
        for (state, sym), nextStates in nfa.transitions.items():
            if state == startState and sym == symbol:
                nextStates.add(endState)
                return nfa
        nfa.transitions[(startState, symbol)] = {endState}
        return nfa

    def singleStartStateNFA(self) -> 'NFA':
        if len(self.startStates) == 1:
            return self
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
        if len(self.finalStates) == 1:
            return self
        from copy import deepcopy
        newNfa = deepcopy(self)
        cnt = 0
        while f"q{cnt}" in newNfa.states:
            cnt += 1
        newFinalState = f"q{cnt}"
        newNfa.states.add(newFinalState)
        for finalState in newNfa.finalStates:
            if (finalState, 'ε') in newNfa.transitions:
                newNfa.transitions[(finalState, 'ε')].add(newFinalState)
            else: 
                newNfa.transitions[(finalState, 'ε')] = {newFinalState}
        newNfa.finalStates = {newFinalState}
        return newNfa 

    def regex(self) -> str:
        nfa = self.singleStartStateNFA().singleFinalStateNFA()

        def R(startState: str, states: set[str], finalState: str) -> str:
            if len(states) == 0:
                alphabet = set()
                for (state, symbol), nextStates in nfa.transitions.items():
                    if state == startState and finalState in nextStates:
                        alphabet.add(symbol) 
                if startState != finalState:
                    if len(alphabet) == 0:
                        return 'φ'
                    else:
                        return '+'.join(alphabet)
                if startState == finalState:
                    if 'ε' not in alphabet:
                        alphabet.add('ε')
                    return '+'.join(alphabet)
            else:
                r = states.pop()
                X = states
                return f"(({R(startState, X, finalState)})+({R(startState, X, r)})({R(r, X, r)})*({R(r, X, finalState)}))"

        return R(list(nfa.startStates)[0], nfa.states, list(nfa.finalStates)[0])

    def reverse(self) -> 'NFA':
        reversedNfa = NFA(
            states=self.states,
            alphabet=self.alphabet,
            transitions=dict(),
            startStates=self.finalStates,
            finalStates=self.startStates
        )
        transMap: dict[tuple[str, str], set[str]] = dict()
        for (state, symbol), nextStates in self.transitions.items():
            for nextState in nextStates:
                if (nextState, symbol) not in transMap:
                    transMap[(nextState, symbol)] = set()
                if state not in transMap[(nextState, symbol)]:
                    transMap[(nextState, symbol)].add(state)
        reversedNfa.transitions = transMap
        return reversedNfa

    def grammar(self) -> 'Grammar':
        from pykleene.grammar import Grammar
        from pykleene.utils import _getNextLetter
        from copy import deepcopy
        nfa = self.singleStartStateNFA()
        grammar = Grammar(
            startSymbol=None,
            terminals=nfa.alphabet,
            nonTerminals=set(),
            productions=dict()
        )
        stateToSymbol = dict()
        currSymbol = 'A'
        for (state, symbol), nextStates in nfa.transitions.items():
            if state not in stateToSymbol:
                stateToSymbol[state] = currSymbol
                currSymbol = _getNextLetter(currSymbol)
            for nextState in nextStates:
                if nextState not in stateToSymbol:
                    stateToSymbol[nextState] = currSymbol
                    currSymbol = _getNextLetter(currSymbol)
            for nextState in nextStates:
                lhs = stateToSymbol[state]
                rhs = (symbol if symbol != 'ε' else '') + stateToSymbol[nextState]
             
                if lhs not in grammar.productions:
                    grammar.productions[lhs] = set()
                grammar.productions[lhs].add(rhs)

        for _, value in stateToSymbol.items():
            grammar.nonTerminals.add(value)

        nfaStartStates = deepcopy(nfa.startStates)
        grammar.startSymbol = stateToSymbol[nfaStartStates.pop()]

        for state in nfa.finalStates:
            if stateToSymbol[state] not in grammar.productions: 
                grammar.productions[stateToSymbol[state]] = set()
            grammar.productions[stateToSymbol[state]].add('ε')

        return grammar

    def image(self, dir: str = None, save: bool = False) -> 'graphviz.Digraph':
        from pykleene._config import graphvizConfig 

        dot = graphviz.Digraph(**graphvizConfig)

        for state in self.states:
            if state in self.finalStates:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        for startState in self.startStates:
            dot.node(f'{id(startState)}', shape='point', label='')
            dot.edge(f'{id(startState)}', startState)

        for (state, symbol), nextStates in self.transitions.items():
            for nextState in nextStates:
                dot.edge(state, nextState, label=symbol)

        if dir and save:
            try:
                dot.render(f"{dir}/<nfa>{id(self)}", format='png', cleanup=True)
            except Exception as e:
                print(f"Error while saving image: {e}")

        return dot

    def epsilonClosure(self, state: str) -> set[str]:
        closure = set()
        closure.add(state)
        queue = [state]
        while len(queue) > 0:
            currentState = queue.pop(0)
            for (s, symbol), nextStates in self.transitions.items():
                if s == currentState and symbol == 'ε':
                    for nextState in nextStates:
                        if nextState not in closure:
                            closure.add(nextState)
                            queue.append(nextState)
        return closure

    def nextStates(self, state: str, symbol: str) -> set[str]:
        for (s, sym), nStates in self.transitions.items():
            if s == state and sym == symbol:
                return nStates
        return set()

    def dfa(self) -> 'DFA':
        from pykleene.dfa import DFA
        def closure(state: str, symbol: str) -> set[str]:
            closure = set()

            closure = closure | nfa.nextStates(state, symbol)

            for nextState in nfa.epsilonClosure(state):
                closure = closure | nfa.nextStates(nextState, symbol)

            for nextState in nfa.nextStates(state, symbol):
                closure = closure | nfa.epsilonClosure(nextState)

            for nextState in nfa.epsilonClosure(state):
                for nextNextState in nfa.nextStates(nextState, symbol):
                    closure = closure | nfa.epsilonClosure(nextNextState)
            
            return closure

        from pprint import pprint
        nfa = self.singleStartStateNFA()
        nfa = nfa.singleFinalStateNFA()

        # nfa.image().view()

        # pprint(nfa.__dict__)

        alphabet: set[str] = self.alphabet
        transitions: dict[tuple[str, str], str] = dict()

        startState = nfa.epsilonClosure(list(nfa.startStates)[0])

        states = set()
        states.add(str(sorted(startState)))
        queue: list[set[str]] = [startState]

        startState = str(sorted(startState)) 

        finalStates = set()

        while len(queue) > 0:
            dfaState = queue.pop(0)
            for symbol in alphabet:
                nextDfaState = set()
                for state in dfaState:
                    nextDfaState = nextDfaState | closure(state, symbol)
                transitions[(str(sorted(dfaState)), symbol)] = str(sorted(nextDfaState))
                if len(dfaState & nfa.finalStates) > 0 and str(sorted(dfaState)) not in finalStates:
                    finalStates.add(str(sorted(dfaState)))
                if str(sorted(nextDfaState)) not in states:
                    queue.append(nextDfaState)
                    states.add(str(sorted(nextDfaState)))

        dfa = DFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            startState=startState,
            finalStates=finalStates
        )

        return dfa