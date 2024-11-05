from enum import Enum
from datetime import datetime, timedelta

class Weather(Enum):
    SUNNY = "sunny"
    OVERCAST = "overcast"
    RAINING = "raining"
    SNOWING = "snowing"

class simulationEngine:
    """This is the main class for the simulation engine.
    Anything that should be considered "global" can go here."""

    def __init__(self, weather: Weather = None, time: datetime = None, time_since_rain: int = 0):
        self.weather = weather if weather is not None else Weather.SUNNY
        self.time = time if time is not None else datetime.now()
        self.time_since_rain = time_since_rain

    def getWeather(self) -> Weather:
        return self.weather

    def setWeather(self, weather: Weather):
        self.weather = weather

    def getTime(self) -> datetime:
        return self.time

    def getTimeSinceRain(self) -> int:
        return self.time_since_rain
