# download to data folder
import requests
from pydantic import BaseModel


class Data(BaseModel):
    """A Data object that can be used to represent downloaded data."""

    pass


def download_data():
    """Download data, validate and write"""
    pass
