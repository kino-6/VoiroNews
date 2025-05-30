from abc import ABC, abstractmethod


class TTSStrategy(ABC):
    @abstractmethod
    def speak(self, text: str):
        pass
