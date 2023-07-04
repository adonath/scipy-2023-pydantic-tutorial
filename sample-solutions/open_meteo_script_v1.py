from datetime import date, datetime
from enum import Enum
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd
import requests
from pydantic import (
    BaseModel,
    NonNegativeFloat,
    PositiveFloat,
    PositiveInt,
    confloat,
    validate_arguments,
)

ABSOLUTE_ZERO_C = -273.15


class DatetimeUnit(Enum):
    ISO_8601 = "iso8601"
    UNIX_TIME = "unixtime"


class TemperatureUnit(Enum):
    CELSIUS = "°C"
    FAHRENHEIT = "°F"


class HourlyUnits(BaseModel):
    time: DatetimeUnit
    temperature_2m: TemperatureUnit


class HourlyData(BaseModel):
    time: list[datetime]
    temperature_2m: list[Union[float, None]]


class OpenMeteoResponse(BaseModel):
    latitude: confloat(ge=-90.0, le=90.0)
    longitude: confloat(ge=-180.0, le=180.0)
    generationtime_ms: PositiveFloat
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    hourly_units: HourlyUnits
    hourly: HourlyData


class WeatherData(BaseModel):
    day_of_year: list[PositiveInt]
    temp_daily_avg: list[confloat(ge=ABSOLUTE_ZERO_C)]
    temp_daily_std: list[NonNegativeFloat]


class WeatherDatasets(BaseModel):
    datasets: dict[str, WeatherData]


def fetch_recent_weather_data() -> OpenMeteoResponse:
    api_endpoint = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 30.2672,
        "longitude": -97.7431,
        "hourly": "temperature_2m",
        "timezone": "GMT",
        "start_date": "2023-01-01",
        "end_date": date.today(),
    }

    response = requests.get(url=api_endpoint, params=params)

    return OpenMeteoResponse.parse_raw(response.content)


def compute_daily_averages(weather_data: OpenMeteoResponse) -> WeatherData:
    weather_data_df = pd.DataFrame(
        data={
            "time": weather_data.hourly.time,
            "temperature": weather_data.hourly.temperature_2m,
        },
    )
    weather_data_df["day_of_year"] = weather_data_df.time.dt.day_of_year

    daily_averages = (
        weather_data_df.groupby("day_of_year")
        .temperature.agg(("mean", "std"))
        .rename(columns={"mean": "temp_daily_avg", "std": "temp_daily_std"})
        .reset_index()
        .to_dict(orient="list")
    )

    return WeatherData(**daily_averages)


@validate_arguments
def plot_data(daily_averages_2023: WeatherData) -> None:
    plt.plot(
        daily_averages_2023.day_of_year,
        daily_averages_2023.temp_daily_avg,
        color="red",
        label="2023 daily average",
    )

    plt.legend(loc="lower center")
    plt.xticks(
        ticks=(1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335),
        labels=(
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ),
    )
    plt.xlabel("Month")
    plt.ylabel("Temperature (C)")
    plt.title("Austin, TX Time Series Temperatures")

    plt.show()


def main():
    weather_data_2023 = fetch_recent_weather_data()
    daily_averages_2023 = compute_daily_averages(weather_data_2023)

    plot_data(daily_averages_2023=daily_averages_2023)


if __name__ == "__main__":
    main()
