from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.data: list[tuple[int, str]] = []
        self.rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        result = self.data.pop(0)
        return result


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        elif isinstance(data, (list)):
            for num in data:
                if not isinstance(num, (int, float)):
                    return False
            return True
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper numeric data")
        if not isinstance(data, (list)):
            data = [data]
        for val in data:
            self.data.append((self.rank, str(val)))
            self.rank += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (str)):
            return True
        elif isinstance(data, (list)):
            for val in data:
                if not isinstance(val, (str)):
                    return False
            return True
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper text data")
        if not isinstance(data, (list)):
            data = [data]
        for val in data:
            self.data.append((self.rank, str(val)))
            self.rank += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            for key, val in data:
                if not (isinstance(key, str) and isinstance(val, str)):
                    return False
            return True
        elif isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                for chk_dict in data:
                    for key, val in chk_dict.items():
                        if not (isinstance(key, str) and isinstance(val, str)):
                            return False
                return True
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper format data")
        if not isinstance(data, list):
            data = [data]
        for val in data:
            self.data.append((self.rank,
                              f"{val['log_level']}: {val['log_message']}"))
            self.rank += 1


class DataStream:
    def __init__(self) -> None:
        self.processor: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processor.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for elem in stream:
            for proc in self.processor:
                if proc.validate(elem):
                    proc.ingest(elem)
                    break
            else:
                print(f"DataStream error - "
                      f"Can't process element in stream: {elem}")

    def print_processors_stats(self) -> None:
        if not self.processor:
            print("No processor found, no data")
            return
        for proc in self.processor:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            print(
                f"{name}: total {proc.rank} items processed, "
                f"remaining {len(proc.data)} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    print("== DataStream statistics ==")

    stream = DataStream()
    stream.print_processors_stats()

    data = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]

    print("\nRegistering Numeric Processor\n")
    stream.register_processor(NumericProcessor())
    print(f"Send first batch of data on stream: {data}")
    stream.process_stream(data)

    print("== DataStream statistics ==")
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())
    print("Send the same batch again")
    stream.process_stream(data)

    print("== DataStream statistics ==")
    stream.print_processors_stats()

    print("\nConsume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        stream.processor[0].output()
    for _ in range(2):
        stream.processor[1].output()
    stream.processor[2].output()

    print("== DataStream statistics ==")
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
