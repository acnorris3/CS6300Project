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

if __name__ == "__main__":
    assert (simulationEngine().getTime() - datetime.now()) < timedelta(seconds=1)
    assert simulationEngine().getWeather() == Weather.SUNNY
    assert simulationEngine(weather=Weather.RAINING).getWeather() == Weather.RAINING
    assert simulationEngine().getTimeSinceRain() == 0
    assert simulationEngine(time=datetime(2020, 1, 1)).getTime() == datetime(2020, 1, 1)
    assert simulationEngine(time_since_rain=5).getTimeSinceRain() == 5
    print("all SimulationEngine class tests passed")