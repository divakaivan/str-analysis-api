from enum import Enum
from src.analyzers.word_count import WordCountAnalyser
from src.analyzers.semantic import SemanticAnalyser

ANALYZERS = [
    WordCountAnalyser,
    SemanticAnalyser,
]


def register_analyzers(registry):
    for ANALYZER in ANALYZERS:
        registry.register(ANALYZER)


AnalysesTypes = Enum(
    "AnalysesTypes",
    {cls.name: cls.name for cls in ANALYZERS},
    type=str,
)


class AnalyserRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, analyser_cls):
        self._registry[analyser_cls.name] = analyser_cls
        return analyser_cls

    def get(self, name: str):
        if name not in self._registry:
            return None
        return self._registry[name]()
