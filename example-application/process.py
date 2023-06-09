# process from data folder to output folder
from pydantic import BaseModel


class DataProcessor(BaseModel):
    """A DataProcessor object that can be used to process data."""

    method: str = "default"

    def run(self, data):
        """Process data."""
        return data
