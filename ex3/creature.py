from abc import ABC, abstractmethod
from .capability import TransformCapability as Transform


class Creature(ABC):
    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return (f"{self.name} is a {self.type} type Creature")


class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return (f"{self.name} uses Ember!")


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        return (f"{self.name} uses Flamethrower!")


class Shiftling(Creature, Transform):
    def __init__(self) -> None:
        super().__init__("Shiftling", "Normal")
        self.transformed = False

    def transform(self) -> str:
        self.transformed = True
        return (f"{self.name} shifts into a sharper form!")

    def revert(self) -> str:
        self.transformed = False
        return (f"{self.name} returns to normal.")

    def attack(self) -> str:
        if self.transformed:
            return (f"{self.name} performs a boosted strike!")
        else:
            return (f"{self.name} attacks normally.")


class Morphagon(Creature, Transform):
    def __init__(self) -> None:
        super().__init__("Morphagon", "Normal/Dragon")
        self.transformed = False

    def transform(self) -> str:
        self.transformed = True
        return (f"{self.name} morphs into a dragonic battle form!")

    def revert(self) -> str:
        self.transformed = False
        return (f"{self.name} stabilizes its form.")

    def attack(self) -> str:
        if self.transformed:
            return (f"{self.name} performs a boosted strike!")
        else:
            return (f"{self.name} attacks normally.")
