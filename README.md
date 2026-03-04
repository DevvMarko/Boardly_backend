# Boardly Task Board API

A task management backend API built with Flask and PostgreSQL. It allows users to create workspaces with unique 4-character codes and manage tasks seamlessly without exposing sequential IDs.

> **Important Note:**
> This repository contains the backend code for the Boardly application.

---

## Features

* **Board Management:** Create, update, and delete workspaces (boards). Each board gets a unique 4-character code for easy and secure sharing.
* **Task Management:** Add, edit, change status, and delete tasks within specific boards. Tasks support icons and multiple statuses.
* **RESTful Endpoints:** Provides a clean interface for integrating front-end applications, returning consistent JSON responses complete with CORS support.
* **Production Ready:** Includes production deployment configuration out-of-the-box using the Waitress WSGI server.

## Tech Stack

* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
* ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
* ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
* ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)

---

## How to use / Quick Start

To interact with the API, send HTTP requests to the available endpoints.
No visual interface is provided in this repository; use client tools like Postman, Thunder Client, curl, or integrate it with a frontend application.

1. Ensure the server is running on `http://localhost:5000` (or your deployment URL).
2. Create a board using `POST /api/boards`. The request body should be: `{"board_name": "My Board", "board_description": "Work items"}`. This will return a unique board code.
3. Access the created board and its tasks using a `GET` request to: `/api/boards/<board_code>`.

---

## Local Development

Instructions for developers on how to run the API locally and modify the code.

### Prerequisites

* Python 3.9+ 
* PostgreSQL Database running locally or remotely

### Steps

1. Clone the repository and navigate to the backend directory:
   ```bash
   git clone [Repository Link]
   cd path/to/backend
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `backend` directory and add your database connection string:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/your_db_name
   ```

5. Run the application in development mode (with active Flask debugger):
   ```bash
   python main.py --dev
   ```

6. Or, run the application in production mode natively using Waitress:
   ```bash
   python main.py
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Project created by [@DevvMarko](https://github.com/DevvMarko) and I invite you to visit the author's portfolio page [mbarchanski.pl](https://mbarchanski.pl)
