from pykleene.symbols import Symbols
import graphviz

class TM:
    states: set[str]
    inputAlphabet: set[str]
    tapeAlphabet: set[str]
    startState: str
    transitions: dict[tuple[str, str], tuple[str, str, str]]
    leftEndMarker: str 
    blankSymbol: str 
    acceptState: str
    rejectState: str

    tapeLength: int = int(1e6)

    def _setNone(self) -> None:
        for key, _ in self.__annotations__.items():
            setattr(self, key, None)

    def isValid(self) -> bool:
        assert self.inputAlphabet <= self.tapeAlphabet, f"Input alphabet {self.inputAlphabet} not a subset of tape alphabet {self.tapeAlphabet}"
        if self.startState: assert self.startState in self.states, f"Start state {self.startState} not in states"
        if self.acceptState: assert self.acceptState in self.states, f"Accept state {self.acceptState} not in states"
        if self.rejectState: assert self.rejectState in self.states, f"Reject state {self.rejectState} not in states"
        if self.leftEndMarker: assert self.leftEndMarker in self.tapeAlphabet, f"Left end marker {self.leftEndMarker} not in tape alphabet {self.tapeAlphabet}"
        if self.blankSymbol: assert self.blankSymbol in self.tapeAlphabet, f"Blank symbol {self.blankSymbol} not in tape alphabet"
        for (state, symbol), (nextState, writeSymbol, direction) in self.transitions.items():
            assert state in self.states, f"State {state} not in states"
            assert symbol in self.tapeAlphabet, f"Symbol {symbol} not in tape alphabet"
            assert nextState in self.states, f"Next state {nextState} not in states"
            assert writeSymbol in self.tapeAlphabet, f"Write symbol {writeSymbol} not in tape alphabet"
            assert direction in ['L', 'R', 'S'], f"Direction {direction} not in ['L', 'R', 'S']"
        return True

    def __init__(self, 
                 states: set[str] = set(), 
                 inputAlphabet: set[str] = set(), 
                 tapeAlphabet: set[str] = set(), 
                 startState: str = None,
                 transitions: dict[tuple[str, str], tuple[str, str, str]] = dict(),
                 leftEndMarker: str = None,
                 blankSymbol: str = None,
                 acceptState: str = None,
                 rejectState: str = None):

        self.states = states
        self.inputAlphabet = inputAlphabet
        self.tapeAlphabet = tapeAlphabet
        self.startState = startState
        self.transitions = transitions
        self.leftEndMarker = leftEndMarker
        self.blankSymbol = blankSymbol
        self.acceptState = acceptState
        self.rejectState = rejectState
        try:
            self.isValid()
        except AssertionError as e:
            print(e)
            self._setNone()

    def loadFromJSONDict(self, jsonDict: dict) -> None:
        self.states = set(jsonDict['states'])
        self.inputAlphabet = set(jsonDict['inputAlphabet'])
        self.tapeAlphabet = set(jsonDict['tapeAlphabet'])
        self.startState = jsonDict['startState']
        self.transitions = dict()
        for [state, symbol, nextState, writeSymbol, direction] in jsonDict['transitions']:
            assert (state, symbol) not in self.transitions, f"Multiple transitions for state {state} and symbol {symbol}"
            self.transitions[(state, symbol)] = (nextState, writeSymbol, direction)
        self.leftEndMarker = jsonDict['leftEndMarker']
        self.blankSymbol = jsonDict['blankSymbol']
        self.acceptState = jsonDict['acceptState']
        self.rejectState = jsonDict['rejectState']
        try:
            self.isValid()
        except AssertionError as e:
            print(e)
            self._setNone()

    def image(self, dir: str = None, save: bool = False, monochrome: bool = False) -> graphviz.Digraph:
        from pykleene._config import graphvizConfig, graphvizAttrConfig, graphvizEdgeConfig
        from pykleene.utils import randomDarkColor
        from pprint import pprint

        dot = graphviz.Digraph(**graphvizConfig)

        dot.attr(**graphvizAttrConfig)

        for state in self.states:
            if state == self.startState:
                dot.node(state, shape='circle', color='black', fontcolor='black')
            elif state == self.acceptState:
                dot.node(state, shape='doublecircle', color='darkgreen', fontcolor='darkgreen')
            elif state == self.rejectState:
                dot.node(state, shape='doublecircle', color='darkred', fontcolor='darkred')
            else:
                dot.node(state, shape='circle')

        if monochrome: color = 'black'
        else: color = randomDarkColor()
        dot.node(f'{id(self.startState)}', shape='point', label='', color=color, fontcolor=color)
        dot.edge(f'{id(self.startState)}', self.startState, **graphvizEdgeConfig, color=color, fontcolor=color)

        for (state, readSymbol), (nextState, writeSymbol, direction) in self.transitions.items():
            if monochrome: color = 'black'
            else: color = randomDarkColor()
            dot.edge(state, nextState, label=f"  {readSymbol}|({writeSymbol}, {direction})  ", **graphvizEdgeConfig, color=color, fontcolor=color)

        if dir and save:
            try:
                dot.render(f"{dir}/<tm>{id(self)}", format='png', cleanup=True)
            except Exception as e:
                print(f"Error while saving image: {e}")

        return dot

    def accepts(self, inputString: str, verbose: bool = False) -> tuple[bool, str]:
        # from pprint import pprint
        # pprint(self.__dict__)
        tape = [self.blankSymbol] * self.tapeLength
        tape[1:1+len(inputString)] = list(inputString)
        tape[0] = self.leftEndMarker
        horizon = (len(inputString) - 1) + 1
        head = 0
        state = self.startState
        while state not in [self.acceptState, self.rejectState]:
            assert head >= 0 and head < self.tapeLength, f"Read/Write head out of bounds: {head}"
            assert tape[head] in self.tapeAlphabet, f"Symbol {tape[head]} not in tape alphabet"
            horizon = max(horizon, head)
            if verbose:
                print(f"{''.join(tape[:horizon+1])} | ({state}, {head})")
            if state == self.acceptState or state == self.rejectState:
                break
            readSymbol = tape[head]
            if (state, readSymbol) in self.transitions:
                nextState, writeSymbol, direction = self.transitions[(state, readSymbol)]
                tape[head] = writeSymbol
                if direction == 'L':
                    head -= 1
                elif direction == 'R':
                    head += 1
                elif direction == 'S':
                    pass
                else:
                    assert False, f"Invalid direction {direction}"
                state = nextState
            else:
                assert False, f"No transition for state {state} and symbol {readSymbol}"
        if state == self.acceptState:
            return True, ''.join(tape[:horizon+1])
        elif state == self.rejectState:
            return False, ''.join(tape[:horizon+1])
        assert False, f"TM halted in undefined state: {state}"

