from typing import Dict, List, Union

DFA = Dict[str, int | List[str] | List[List[str]]] 
NFA = Dict[str, str | List[str] | List[List[str | List[str]]]]
RG = Dict[str, Dict[str, List[str]] | List[str]]