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

## Unit Tests
When writing classes, please include your tests at the bottom of the file. By controlling your tests with a
```
if __name__ == "__main__":
    assert testthing == True
    print("All {this class} tests passed")
```
You can print out confirmation of test passes only when running that specific file (and not when importing it in another file)