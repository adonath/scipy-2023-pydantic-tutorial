import yaml
from pydantic import BaseModel


class Config(BaseModel):
    """A Config object that can be used to read and write YAML files."""

    name: str = "default"
    models: list = ["model1", "model2"]

    def write(self, filename: str):
        """Writes the Config object to a YAML file.

        Parameters
        ----------
        filename : str
            The name of the YAML file to write.
        """
        with open(filename, "w") as file:
            yaml.dump(self.dict(), file)

    @classmethod
    def read(cls, filename: str):
        """Reads a YAML file and returns a Config object.

        Parameters
        ----------
        filename : str
            The name of the YAML file to read.

        Returns
        -------
        config : Config
            A Config object.
        """
        with open(filename) as file:
            config = yaml.safe_load(file)

        return cls(**config)
