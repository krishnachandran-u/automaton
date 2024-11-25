from pykleene.tm import TM
from typing import Callable
class LBA(TM):
    rightEndMarker: str

    def __init__(self, 
                 states: set[str] = set(), 
                 inputAlphabet: set[str] = set(), 
                 tapeAlphabet: set[str] = set(), 
                 startState: str = None, 
                 transitions: dict[tuple[str, str], tuple[str, str, str]] = dict(), 
                 leftEndMarker: str = None, 
                 rightEndMarker: str = None,
                 blankSymbol: str = None,
                 acceptState: str = None, 
                 rejectState: str = None):
        self.rightEndMarker = rightEndMarker
        super().__init__(states, 
                         inputAlphabet, 
                         tapeAlphabet, 
                         startState, 
                         transitions, 
                         leftEndMarker, 
                         blankSymbol, 
                         acceptState, 
                         rejectState)
        self.tapeLength = None
        try:
            if self.rightEndMarker: assert self.rightEndMarker in self.tapeAlphabet, f"Right end marker {self.rightEndMarker} not in tape alphabet {self.tapeAlphabet}"
        except AssertionError as e:
            print(e)
            self._setNone()

    def loadFromJSONDict(self, jsonDict: dict) -> None:
        self.rightEndMarker = jsonDict['rightEndMarker']
        super().loadFromJSONDict(jsonDict)
        try:
            if self.rightEndMarker: assert self.rightEndMarker in self.tapeAlphabet, f"Right end marker {self.rightEndMarker} not in tape alphabet {self.tapeAlphabet}"
        except AssertionError as e:
            print(e)
            self._setNone()

    def accepts(self, inputString: str, verbose: bool = False, tapeLenFunc: Callable[[int], int] = None) -> tuple[bool, str]:
        assert tapeLenFunc, "tapeLenFunc not provided"
        self.tapeLength = tapeLenFunc(len(inputString))
        tape = [self.blankSymbol] * self.tapeLength
        assert len(inputString) <= self.tapeLength - 2, f"Input string {inputString} too long for tape length {self.tapeLength}"
        tape[1:1+len(inputString)] = list(inputString)
        tape[0] = self.leftEndMarker
        tape[self.tapeLength-1] = self.rightEndMarker
        head = 1
        state = self.startState
        while state not in [self.acceptState, self.rejectState]:
            assert head >= 0 and head < self.tapeLength, f"Read/Write head out of bounds: {head}"
            assert tape[head] in self.tapeAlphabet, f"Symbol {tape[head]} not in tape alphabet"
            if verbose:
                print(f"{''.join(tape)} | ({state}, {head})")
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
            return True, ''.join(tape)
        elif state == self.rejectState:
            return False, ''.join(tape)
        assert False, f"TM halted in undefined state: {state}" 


