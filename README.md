# CS6300 Project


## Purpose

Simulate an automated lawn mower.

## Setup/Dependency Management


- Clone this repo

- Create a virtual environment
```
python -m venv env
```

- Activate environment (for windows)
```
.\env\Scripts\activate
```
- (for Unix)
```
source ./env/bin/activate
```

- Install the python libraries
```
pip install -r .\requirements.txt
```

- Verify your libraries are installed

```
pip list -v
```

- After adding new dependencies
```
pip freeze > requirements.txt
```

![image](https://github.com/user-attachments/assets/a469e716-64ab-4482-89eb-11869e9db7a2)

## Tests
THIS INFORMATION HAS BEEN UPDATED
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

## Definition of done:
-	Add assert statements to make sure any future potential breaking changes are caught
-	Git pull
-	Merge your code, verify any conflicts
-	Run the code and verify nothing is broken
-	Git push
-	Complete task in GitHub by moving to Done and enter “Time Spent On Task”

## GitHub Project
### How to assign a task to an individual
- Click on the text in the task card.
- A popup window should open on the right side of the screen
- Click on "Assignees" and select one or more names to assing that task to an individual(s)
- Also enter the estimated number of hours that this task should take
- Select a sprint that this task should take place in

### To see your own assigned items:
- Click tab titled "My Items".
- You can see what tasks have been assigned to you

### To see tasks that everyone is working on in the current sprint:
- Click tab titled "Current Iteration"
- You can see all the tasks that have been assigned to anyone on the team, for the current sprint

### To see tasks from the previous sprint (helpful for burndown chart and sprint review):
- Click tab titled "Previous Iteration"
- Shows all tasks that have been assigned to the prevous sprint.
- Can see what was completed, who it was assigned to, how long the task was estimated to take vs how long it actually took.


## Documentation

To avoid this README from growing too much there is now a folder where specifc information can now be found.
Like this [doc](/docs/how-to-add-pics.md) on how to add pictures to readme files.


## Basic info about pygame and our specific use case of it.

Please take a look at this [doc](/docs/pygame_basics.md)