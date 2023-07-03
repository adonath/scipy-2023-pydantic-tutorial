from typing import Optional

from pydantic import BaseModel

data_samples = [
    {
        "date": "2023-05-20",
        "temperature": 62.2,
        "isCelsius": False,
        "airQualityIndex": "24",
        "sunriseTime": "01:26",
        "sunsetTime": "00:00",
    },
    {
        "date": "2023-05-21",
        "temperature": "64.4",
        "isCelsius": "false",
        "airQualityIndex": 23,
        "sunriseTime": "01:10",
        "sunsetTime": "00:16",
    },
    {
        "date": "2023-05-22",
        "temperature": 14.4,
        "airQualityIndex": 21,
    },
]


class WeatherData(BaseModel):

    date: str
    temperature: float
    isCelsius: bool = True
    airQualityIndex: int
    sunriseTime: Optional[str]
    sunsetTime: Optional[str]

    def convert_temperature_to_celsius(self) -> None:
        if not self.isCelsius:
            self.temperature = (self.temperature - 32) * 5 / 9
            self.isCelsius = True

    def convert_temperature_to_fahrenheit(self) -> None:
        if self.isCelsius:
            self.temperature = self.temperature * 9 / 5 + 32
            self.isCelsius = False


def main() -> None:

    weather_data = [WeatherData(**data_sample) for data_sample in data_samples]

    for day in weather_data:
        day.convert_temperature_to_celsius()

    mean_temperature = sum(day.temperature for day in weather_data) / len(weather_data)
    print(
        f"The mean temperature in Murmansk, Russia between May 20 and May 22 was "
        f"{mean_temperature:.1f} degrees celsius"
    )


if __name__ == "__main__":
    main()
