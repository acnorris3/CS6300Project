To ensure repo-wide testing, Brendan proposes that we move to using `pytest`. Pytest has been added to `requirements.txt` so if you install off of that, you already have pytest.
### How to use pytest
do `pytest` in terminal
### How to write tests for pytest
Pytest will only pick up your tests if they're in a file that starts `test_` and if they're contained in a function that starts `def test_`. Once both of those are satisfied, running `pytest` will run the code contained in your function and, if there are no errors, consider that function to be a successfully completed test
### Why bother using pytest?
1. pytest can hit a failure in a test and continue running other tests
2. pytest tests the entire repo in a single go
### Can I get an example?
Yeah for sure! Please refer to `./simulation/test_simulationEngine.py` and `./simulation/simulationEngine.py`. Note also that you can write multiple test functions inside of a single test file if needed/desired, they just need to all start with `def test_`

