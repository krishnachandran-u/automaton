# Pykleene

Pykleene is a powerful Python library designed to make working with automata theory and formal languages accessible and intuitive. Whether you're a student learning theoretical computer science, a researcher working on language processing, or a developer implementing formal verification systems, pykleene provides the tools you need to work with various types of automata and grammars.

See [pykleene documentation](https://pykleene.vercel.app/).

## Getting Started

To begin using pykleene, follow these simple steps:
- make sure you have `Graphviz` installed on your system.
- Install pykleene using pip: `pip install pykleene`
- Import the necessary components into your Python script
- Start building and simulating automata!

Pykleene supports a wide range of formal language concepts, from basic finite automata to complex Turing machines. The library is designed with both educational and practical applications in mind, featuring clear APIs and comprehensive documentation to help you get started quickly.

## Key Features

> "Automata theory is a fundamental pillar of computer science, and pykleene aims to make these concepts tangible and practical through clean, intuitive Python implementations."

Our library includes support for:
- Deterministic Finite Automata (DFA)
- Non-deterministic Finite Automata (NFA)
- Regular Expressions
- Pushdown Automata
- Linear Bounded Automata and Turing Machines
- Various Grammar Types (Regular to Unrestricted)
- Regular Expressions

## Code Example

Here's a simple example of checking the isomorphism of two DFAs: 

```python showLineNumbers
from pykleene.dfa import DFA
from typing import Dict
import json
import os

# Define input and output paths directly
INPUT_FILE_PATH = 'path/to/your/input/dfas.json'  # Replace with actual path to the input file
OUTPUT_DIR_PATH = 'path/to/output/directory'  # Replace with actual output directory path

FILENAME = 'dfas.json'

if __name__ == '__main__':
    DFAs: Dict[str, DFA]
    
    # Load the DFAs from the JSON file
    with open(INPUT_FILE_PATH, 'r') as file:
        DFAs = json.load(file)

    # Process each DFA
    for dfaName, dfaData in DFAs.items():
        dfa = DFA()
        dfa.loadFromJSONDict(dfaData)
        
        # Generate the DFA image and save it in the output directory
        output_file_path = os.path.join(OUTPUT_DIR_PATH, f'{dfaName}_dfa.png')
        dfa.image(dir=output_file_path, save=True)
        
        # Update the DFAs dictionary with the processed DFA
        DFAs[dfaName] = dfa

    # Compare the DFAs for isomorphism (equivalence)
    for dfaName1, dfa1 in DFAs.items():
        for dfaName2, dfa2 in DFAs.items():
            if dfaName1 != dfaName2:
                if dfa1.isomorphic(dfa2):
                    print(f"{dfaName1} is equivalent to {dfaName2}")
                else:
                    print(f"{dfaName1} is not equivalent to {dfaName2}")
```

## Conclusion

Pykleene strives to be your go-to library for working with formal languages and automata in Python. Whether you're teaching these concepts, learning them, or applying them in practice, our library provides the flexibility and functionality you need. Check out our other documentation sections to dive deeper into specific features and use cases.