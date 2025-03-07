# Ecommerce API

This is an API for an ecommerce application built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. The API allows users to manage products and orders for an ecommerce platform. The application is containerized using **Docker** and connects to a **PostgreSQL** database.

## Features

- Product Management:
  - Create, list, and manage products in the system.
- Order Management:
  - Create, view, and manage orders.
- Swagger UI Documentation:
  - API documentation is available at `/docs`.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: For containerization.
- **Docker Compose**: For managing multi-container Docker applications.
- **Python** (for development, if needed): Version 3.9 or higher.

## Project Structure
ecommerce_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and routes
│   ├── models.py        # Database models (Product, Order)
│   ├── schemas.py       # Pydantic schemas for validation
│   ├── crud.py          # Logic for interacting with DB
│   ├── database.py      # DB setup and session handling
│   └── config.py        # Config for DB connection
├── Dockerfile           # Docker container for app
├── requirements.txt     # List of dependencies
└── README.md            # Project documentation

## Setup and Running the Application

### 1. Clone the Repository

```bash
git clone https://github.com/rishistrive/Ecommerce-API.git
cd ecommerce-api
```

### 2. Create Postgres database user and password 

```bash
CREATE DATABASE ecommerce_db;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'developer';
```

### 3. Rename the .env.example file to .env

### 4. start the application using docker 

```bash
Docker compose up --build
```
