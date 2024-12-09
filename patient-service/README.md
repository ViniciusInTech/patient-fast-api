# FastAPI Patient Management System

## Overview
This is a patient management project using **FastAPI**, **SQLAlchemy**, and **SQLite** as the database. The application provides a RESTful API for patient management with secure authentication.

## Features
* Patient registration, editing, deletion, and querying
* Secure JWT authentication
* Comprehensive data validation
* High-performance API design

## Technologies
* **FastAPI**: Modern API framework
* **Uvicorn**: ASGI server
* **SQLAlchemy**: Database ORM
* **Pydantic**: Data validation
* **JWT**: Secure authentication

## Installation

### Cloning the Repository
```bash
git clone https://github.com/ViniciusInTech/patient-fast-api.git
```

### Docker Setup
Build the Docker image:
```bash
docker build -t fastapi-app .
```

Run the container:
```bash
docker run -d -p 8000:8000 fastapi-app
```

## Authentication
Default credentials:
* **Username**: admin
* **Password**: admin123

## Documentation
Access API documentation at: http://localhost:8000/redoc