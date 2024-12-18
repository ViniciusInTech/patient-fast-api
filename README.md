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
docker-compose build
```

Run the container:
```bash
docker-compose up  
```

## Authentication
Default credentials:
* **email**: admin@admin.com
* **password**: admin123

## Documentation
Access API documentation at: http://localhost:8001/redoc

## Auth-service 
http://localhost:8000/api/login/
http://localhost:8000/api/register/

## patient-service
http://localhost:8001/api/patients/