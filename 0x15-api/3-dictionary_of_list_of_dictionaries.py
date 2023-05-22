#!/usr/bin/python3
"""Exports to-do list data for an employee to JSON format"""

import json
import requests
import sys


if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/"
    users = requests.get("{}users".format(url)).json()
    tasks = requests.get("{}todos".format(url)).json()
    data_dict = {
                user.get("id"): [{"username": user.get("username"),
                                  "task": task.get("title"),
                                  "completed": task.get("completed")}
                                 for task in tasks
                                 if task.get("userId") == user.get("id")]
                for user in users
           }
    # open a new JSON file in write mode
    with open("todo_all_employees.json", "w", newline="") as file:
        json.dump(data_dict, file)
