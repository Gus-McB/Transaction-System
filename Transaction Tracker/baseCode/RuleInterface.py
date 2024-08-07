from abc import ABC, abstractmethod

class RuleInterface(ABC):
    @abstractmethod
    def importRules(self, filePath: str) -> bool:
        pass

    @abstractmethod
    def getRules(self) -> dict:
        pass