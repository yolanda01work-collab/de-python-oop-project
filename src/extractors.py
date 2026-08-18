import csv
import json
from abc import ABC, abstractmethod


class Extractor(ABC):

    @abstractmethod
    def extract(self):
        pass


class CSVExtractor(Extractor):

    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        records = []

        with open(self.file_path, "r", newline="", encoding="utf8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                records.append(row)

        return records


class JSONExtractor(Extractor):

    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):

        with open(self.file_path, "r", encoding="utf8") as file:
            data = json.load(file)

        return data