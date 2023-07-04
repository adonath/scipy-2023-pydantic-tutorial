from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from pydantic import (
    BaseModel,
    NonNegativeFloat,
    PositiveFloat,
    PositiveInt,
    confloat,
    root_validator,
    validate_arguments,
)
from scipy.special import erfinv

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

    @root_validator
    def _root_validator(cls, values: dict[str, Any]) -> dict[str, Any]:
        if len(values["time"]) != len(values["temperature_2m"]):
            raise ValueError("time array and temperature array are not the same length")
        return values


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

    @root_validator
    def assert_valid_temps(cls, values: dict[str, Any]) -> dict[str, Any]:
        min_temp = ABSOLUTE_ZERO_C
        if values["hourly_units"].temperature_2m is TemperatureUnit.FAHRENHEIT:
            min_temp = min_temp * 9 / 5 + 32

        if not all(
            temperature >= min_temp for temperature in values["hourly"].temperature_2m
        ):
            raise ValueError("Some temperatures are below absolute zero")

        return values


class WeatherData(BaseModel):
    day_of_year: list[PositiveInt]
    temp_daily_avg: list[confloat(ge=ABSOLUTE_ZERO_C)]
    temp_daily_std: list[NonNegativeFloat]

    def temp_daily_lower_bound(self, confidence_level: float = 0.95) -> list[float]:
        z_score = np.sqrt(2) * erfinv(confidence_level)
        return [
            temp - z_score * std
            for temp, std in zip(self.temp_daily_avg, self.temp_daily_std)
        ]

    def temp_daily_upper_bound(self, confidence_level: float = 0.95) -> list[float]:
        z_score = np.sqrt(2) * erfinv(confidence_level)
        return [
            temp + z_score * std
            for temp, std in zip(self.temp_daily_avg, self.temp_daily_std)
        ]


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


@validate_arguments
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
def plot_data(
    long_term_daily_averages: WeatherData, daily_averages_2023: WeatherData
) -> None:
    plt.plot(
        long_term_daily_averages.day_of_year,
        long_term_daily_averages.temp_daily_avg,
        color="blue",
        label="Long-term daily average",
    )
    plt.fill_between(
        x=long_term_daily_averages.day_of_year,
        y1=long_term_daily_averages.temp_daily_lower_bound(confidence_level=0.68),
        y2=long_term_daily_averages.temp_daily_upper_bound(confidence_level=0.68),
        color="cyan",
        label="+/- 1 standard deviation",
    )

    plt.plot(
        daily_averages_2023.day_of_year,
        daily_averages_2023.temp_daily_avg,
        color="red",
        label="2023 daily average",
    )
    plt.fill_between(
        x=daily_averages_2023.day_of_year,
        y1=daily_averages_2023.temp_daily_lower_bound(confidence_level=0.68),
        y2=daily_averages_2023.temp_daily_upper_bound(confidence_level=0.68),
        color="pink",
        label="+/- 1 standard deviation",
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


@validate_arguments
def save_data(
    long_term_daily_averages: WeatherData, daily_averages_2023: WeatherData
) -> None:
    fpath_combined_data = Path(__file__).parent / "combined_data.json"
    combined_data = WeatherDatasets(
        datasets={
            "long_term_daily_averages": long_term_daily_averages,
            "weather_data_2023": daily_averages_2023,
        }
    )
    fpath_combined_data.write_text(combined_data.json(indent=2))


def main():
    weather_data_2023 = fetch_recent_weather_data()
    daily_averages_2023 = compute_daily_averages(weather_data_2023)

    fpath_noaa_data = (
        Path(__file__).parent / "exercises_data" / "noaa_long_term_avgs.json"
    )
    long_term_daily_averages = WeatherData.parse_file(fpath_noaa_data)

    plot_data(
        long_term_daily_averages=long_term_daily_averages,
        daily_averages_2023=daily_averages_2023,
    )

    save_data(
        long_term_daily_averages=long_term_daily_averages,
        daily_averages_2023=daily_averages_2023,
    )


if __name__ == "__main__":
    main()
