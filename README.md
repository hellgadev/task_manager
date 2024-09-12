# Task Management API

## Overview

This project implements an API for a task management system using Django.
The API allows for CRUD operations on tasks and includes features such as filtering by status, sorting by creation date,
and searching by title.
It also supports user authentication with token-based access.
Project is dockerized.

## Features

- **CRUD Operations:** Create, view, update, and delete tasks.
- **Task Attributes:** Each task includes a title, description, status (completed/incomplete), and creation date.
- **Filtering:** Filter tasks by status.
- **Sorting:** Sort tasks by creation date.
- **Searching:** Search tasks by title.
- **Authentication:** Token-based authentication allowing different access levels for authenticated and
  non-authenticated users.
- **Testing :** Unit tests for API endpoints.
- **Dockerization :** Docker setup for containerizing the application.

## Installation

1. **Clone the Repository:**

```bash
git clone git@github.com:hellgadev/task_manager.git
cd task_manager
```

2. **Create a Virtual Environment and Install Dependencies:**

```bash
python3.11 -m venv env
source env/bin/activate
```
3. Copy file .env.example, rename it to .env and set variables
```bash
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_URL=
POSTGRES_PORT=
```
3. 
4. **Run the server via docker-compose**
   For the first time run command with ``--build``

```bash
docker-compose up --build
```
4. Verify that server runs properly:
http://localhost:8001

## API Documentation

Refer to [Postman](https://www.postman.com/) collection [here](postman/Task_manager.postman_collection.json)

## Database Access
You can reach Postgres via Adminer at http://localhost:8081/

## Testing

Jump into core container and run tests

```bash
docker exec -it task_manager_core_1 bash
pytest tests/test_api_tasks.py
```

## Built With

* [Docker](https://docs.docker.com/install/) – used for auto-deployment and 
  management the applications and create containers.
* [Docker-compose](https://docs.docker.com/compose/install/) – used for running 
  multiple Docker containers and build and manage them local.
* [Django](https://www.djangoproject.com/) – Web framework.
