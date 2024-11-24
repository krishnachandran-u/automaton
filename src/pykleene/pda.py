import graphviz

class PDA:
    states: set[str]
    inputAlphabet: set[str]
    stackAlphabet: set[str]
    transitions: dict[tuple[str, str, str], set[tuple[str, str]]] 
    startState: str
    initialStackSymbol: str
    finalStates: set[str]

    def _setNone(self) -> None:
        for key, _ in self.__annotations__.items():
            setattr(self, key, None)

    def __init__(self, 
                 states: set[str] = set(), 
                 inputAlphabet: set[str] = set(), 
                 stackAlphabet: set[str] = set(), 
                 transitions: dict[tuple[str, str, str], set[tuple[str, str]]] = dict(),
                 startState: str = None,
                 initialStackSymbol: str = None,
                 finalStates: set[str] = set()) -> None:

        self.states = states
        self.inputAlphabet = inputAlphabet
        self.stackAlphabet = stackAlphabet
        self.transitions = transitions
        self.startState = startState
        self.initialStackSymbol = initialStackSymbol
        self.finalStates = finalStates
        try:
            self.isValid()
        except AssertionError as e:
            print(e)
            self._setNone()

    def isValid(self) -> bool:
        if self.startState: assert self.startState in self.states, f"Start state {self.startState} not in states"
        if self.initialStackSymbol: assert self.initialStackSymbol in self.stackAlphabet, f"Initial stack symbol {self.initialStackSymbol} not in stack alphabet"
        assert self.finalStates <= self.states, f"Final states {self.finalStates} not in states"
        for (state, inputSymbol, stackSymbol), nextConfigs in self.transitions.items():
            for nextState, stackString in nextConfigs:
                assert state in self.states, f"State {state} not in states"
                if inputSymbol and inputSymbol != "ε": assert inputSymbol in self.inputAlphabet, f"Input symbol {inputSymbol} not in input alphabet"
                assert stackSymbol in self.stackAlphabet, f"Stack symbol {stackSymbol} not in stack alphabet"
                assert nextState in self.states, f"Next state {nextState} not in states"
                if stackString != "ε":
                    for symbol in stackString:
                        assert symbol in self.stackAlphabet, f"Symbol {symbol} in stack string not in stack alphabet"
        return True

    def loadFromJSONDict(self, jsonDict: dict) -> None:
        self.states = set(jsonDict['states'])
        self.inputAlphabet = set(jsonDict['inputAlphabet'])
        self.stackAlphabet = set(jsonDict['stackAlphabet'])
        for [state, inputSymbol, stackSymbol, nextState, stackString] in jsonDict['transitions']:
            if (state, inputSymbol, stackSymbol) not in self.transitions:
                self.transitions[(state, inputSymbol, stackSymbol)] = set()
            self.transitions[(state, inputSymbol, stackSymbol)].add((nextState, stackString))
        self.startState = jsonDict['startState']
        self.initialStackSymbol = jsonDict['initialStackSymbol']
        self.finalStates = set(jsonDict['finalStates'])
        from pprint import pprint
        pprint(self.__dict__)
        try:
            self.isValid()
        except AssertionError as e:
            print(e)
            self._setNone()

    def image(self, dir: str = None, save: bool = False, monochrome: bool = False) -> graphviz.Digraph:
        from pykleene._config import graphvizConfig, graphvizAttrConfig, graphvizEdgeConfig
        from pykleene.utils import randomDarkColor

        dot = graphviz.Digraph(**graphvizConfig)

        dot.attr(**graphvizAttrConfig)

        for state in self.states:
            if state in self.finalStates:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        if monochrome: color = 'black'
        else: color = randomDarkColor()
        dot.node(f'{id(self.startState)}', shape='point', label='', color=color, fontcolor=color)
        dot.edge(f'{id(self.startState)}', self.startState, **graphvizEdgeConfig, color=color, fontcolor=color)

        for (state, inputSymbol, stackSymbol), nextConfigs in self.transitions.items():
            for nextState, stackString in nextConfigs:
                if monochrome: color = 'black'
                else: color = randomDarkColor()
                dot.edge(state, nextState, label=f"  {inputSymbol}: {stackSymbol} -> {stackString}  ", **graphvizEdgeConfig, color=color, fontcolor=color)

        if dir and save:
            try:
                dot.render(f"{dir}/pda>{id(self)}", format='png', cleanup=True)
            except Exception as e:
                print(f"Error while saving image: {e}")

        return dot
        
    """
    def accept(self, string: str) -> bool:
        stack = [self.initialStackSymbol]
        state = self.startState
        index = 0
        while index < len(string):
            if (state, string[index], stack[-1]) in self.transitions:
                nextState, stackString = self.transitions[(state, string[index], stack[-1])]
                stack.pop()
                if stackString != "ε":
                    stack += list(stackString)[::-1]
                state = nextState
                index += 1
            else:
                return False
        if state in self.finalStates:
            return True
        else:
            return False
    """

    def isDeterministic(self) -> bool:
        for state in self.states:
            for inputSymbol in self.inputAlphabet:
                for stackSymbol in self.stackAlphabet:
                    nextConfigs = set()
                    if (state, inputSymbol, stackSymbol) in self.transitions:
                        nextConfigs = nextConfigs | self.transitions[(state, inputSymbol, stackSymbol)]
                    if (state, "ε", stackSymbol) in self.transitions:
                        nextConfigs = nextConfigs | self.transitions[(state, "ε", stackSymbol)]
                    if len(nextConfigs) > 1:
                        return False
        return True

    def accepts(self, string: str) -> bool:
        assert self.isDeterministic(), "PDA is not deterministic"
        stack = [self.initialStackSymbol]
        state = self.startState
        index = 0
        while index < len(string):
            if len([t for t in self.transitions if t[0] == state and t[1] == string[index] and t[2] == stack[-1]]) == 1:
                nextState, stackString = [t for t in self.transitions if t[0] == state and t[1] == string[index] and t[2] == stack[-1]][0][3:]
                stack.pop()
                if stackString != "ε":
                    stack += list(stackString)[::-1]
                state = nextState
                index += 1
            elif len([t for t in self.transitions if t[0] == state and t[1] == "ε" and t[2] == stack[-1]]) == 1:
                nextState, stackString = [t for t in self.transitions if t[0] == state and t[1] == "ε" and t[2] == stack[-1]][0][3:]
                stack.pop()
                if stackString != "ε":
                    stack += list(stackString)[::-1]
                state = nextState
            else:
                return False
        if state in self.finalStates or not len(stack):
            return True
        else:
            return False