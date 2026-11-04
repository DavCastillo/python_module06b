from abc import ABC, abstractmethod
from typing import Any, Protocol


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
        return self.data.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(value, (int, float)) for value in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper numeric data")
        values = data if isinstance(data, list) else [data]
        for value in values:
            self.data.append((self.rank, str(value)))
            self.rank += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(value, str) for value in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper text data")
        values = data if isinstance(data, list) else [data]
        for value in values:
            self.data.append((self.rank, value))
            self.rank += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            entries = [data]
        elif isinstance(data, list) and all(
            isinstance(value, dict) for value in data
        ):
            entries = data
        else:
            return False

        return all(
            all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in entry.items()
            )
            for entry in entries
        )

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Got exception: Improper log data")
        values = data if isinstance(data, list) else [data]
        for value in values:
            self.data.append(
                (self.rank, f"{value['log_level']}: {value['log_message']}")
            )
            self.rank += 1


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(value for _, value in data))


class JSONPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        items = []
        for rank, value in data:
            items.append(f'"item_{rank}": "{value}"')
        print("JSON Output:")
        print("{" + ", ".join(items) + "}")


class DataStream:
    def __init__(self) -> None:
        self.processor: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processor.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            for proc in self.processor:
                if proc.validate(element):
                    proc.ingest(element)
                    break
            else:
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processor:
            print("No processor found, no data")
            return
        for proc in self.processor:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            print(
                f"{name}: total {proc.rank} items processed, "
                f"remaining {len(proc.data)} on processor"
            )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processor:
            output: list[tuple[int, str]] = []
            for _ in range(nb):
                if proc.data:
                    output.append(proc.output())
            plugin.process_output(output)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("\nInitialize Data Stream...\n")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors\n")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    first_batch = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {first_batch}")
    print()
    stream.process_stream(first_batch)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVPlugin())
    print()
    stream.print_processors_stats()

    second_batch = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {second_batch}")
    stream.process_stream(second_batch)
    print()
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONPlugin())
    print()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
