# to-do- lis application
This repo contains demo code for the TBC Academy's "intro to python" course's final project

A Python-based To-Do List application with task creation, updating, sorting, and deletion functionalities, along with task persistence using CSV file storage. The application follows object-oriented programming (OOP) principles and is modularized for better code organization.

## Features

- Create tasks with description, priority, status, and optional start and due dates.
- Update existing tasks' description, priority, status, start date, and due date.
- Sort tasks based on description, priority, due date, or creation date.
- Delete tasks by task ID.
- Persist tasks between sessions using CSV file storage.

## Project Structure

├── task.py # Task and StartDateDueDateTask class definitions
├── csv_writer.py # Functions for saving and loading tasks from CSV file
├── todo_app.py # ToDoApp class with task management methods
├── main.py # Entry point for running the application
├── tasks.csv # CSV file for storing tasks (generated at runtime)
└── README.md # Project documentation


