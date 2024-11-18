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
        self.nonTerminals = set(data['nonTerminals'])
        self.terminals = set(data['terminals'])
        for production in data['productions']:
            if production[0] in self.productions:
                self.productions[production[0]].add(production[1])
            else:
                self.productions[production[0]] = set(production[1])
        self.startSymbol = data['startSymbol']

     
