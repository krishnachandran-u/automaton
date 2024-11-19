class Grammar:
    nonTerminals: set[str] = set()
    terminals: set[str] = set()
    productions: dict[str, set[str]] = dict()
    startSymbol: str 

    def __init__(self, 
                 nonTerminals: set[str] = set(), 
                 terminals: set[str] = set(), 
                 productions: dict[str, set[str]] = dict(), 
                 startSymbol: str = None):
        self.nonTerminals = nonTerminals
        self.terminals = terminals
        self.productions = productions
        self.startSymbol = startSymbol

    def loadFromJSONDict(self, data: dict) -> None:
        try:
            newGrammar = Grammar()
            newGrammar.nonTerminals = set(data['nonTerminals'])
            newGrammar.terminals = set(data['terminals'])
            for production in data['productions']:
                if production[0] in newGrammar.productions:
                    newGrammar.productions[production[0]].add(production[1])
                else:
                    newGrammar.productions[production[0]] = set(production[1])
            newGrammar.startSymbol = data['startSymbol']
        except Exception as e:
            print(f"Illegal format: {e}")
        
        if newGrammar.isValid():
            self = newGrammar
        else:
            raise ValueError("Invalid grammar")

    def isValid(self) -> bool:
        for nonTerminal in self.nonTerminals:
            if len(nonTerminal) > 1:
                return False
        for terminal in self.terminals:
            if len(terminal) > 1:
                return False
        if self.startSymbol not in self.nonTerminals:
            return False 
        startSymbolFound = False
        for lhs, productions in self.productions.items():
            if len(lhs) == 0:
                return False
            if lhs == self.startSymbol:
                startSymbolFound = True
            for i, char in enumerate(lhs):
                if char not in self.nonTerminals or char not in self.terminals:
                    return False
            for rhs in productions:
                if len(rhs) == 0:
                    return False
                if rhs == 'ε':
                    continue
                for char in rhs:
                    if char not in self.terminals and char not in self.nonTerminals:
                        return False
        if not startSymbolFound:
            return False
        return True

    def isLeftLinear(self) -> bool:
        if not self.isValid():
            return False

        for lhs, productions in self.productions.items():
            if lhs not in self.nonTerminals:
                return False
            for rhs in productions:
                if len(rhs) == 0:
                    return False
                if rhs == 'ε':
                    continue
                if rhs[0] not in self.terminals or rhs[0] not in self.nonTerminals:
                    return False
                for char in rhs[1:]:
                    if char not in self.terminals:
                        return False
        return True

    def isRightLinear(self) -> bool:
        if not self.isValid():
            return False
        for lhs, productions in self.productions.items():
            if lhs not in self.nonTerminals:
                return False
            for rhs in productions:
                if len(rhs) == 0:
                    return False
                if rhs == 'ε':
                    continue
                if rhs[-1] not in self.terminals or rhs[-1] not in self.nonTerminals:
                    return False
                for char in rhs[:-1]:
                    if char not in self.terminals:
                        return False
        return True
    def isRegular(self) -> bool:
        if not self.valid():
            return False 
        return self.isLeftLinear() or self.isRightLinear()

     
