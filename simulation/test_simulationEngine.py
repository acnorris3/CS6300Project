from datetime import datetime, timedelta
from simulationEngine import simulationEngine, Weather
def test_simulationEngine():
    assert (simulationEngine().getTime() - datetime.now()) < timedelta(seconds=1)
    assert simulationEngine().getWeather() == Weather.SUNNY
    assert simulationEngine(weather=Weather.RAINING).getWeather() == Weather.RAINING
    assert simulationEngine().getTimeSinceRain() == 0
    assert simulationEngine(time=datetime(2020, 1, 1)).getTime() == datetime(2020, 1, 1)
    assert simulationEngine(time_since_rain=5).getTimeSinceRain() == 5
    print("all SimulationEngine class tests passed")