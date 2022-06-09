# Bot - CSC 466 Project Calpass

Bot uses our MySQL DB to answer user queries using Machine Learning.

### Code Structure

* **calpass.py** : Driver file, contains bot implementation.
* **db.py** : Contains DB related functions.
* **fetch_answer.py** : Contains functions related to fetching DB and printing answers.
* **lev_dist.py** : Stale file. Initially, was intended to be used for handling mispellings, but time constraint didn't allow for it.
* **models.py** : Contains Bagging classifier implementation.
* **test_cases.txt** : Contains all test cases used to test our bot's performance.
* **test_split.py** : generates the test.in query file
* **eval.py** : evaluates the accuracy of the tests

### Usage

```python 
python3 calpass.py
```
