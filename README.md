# URL Shortener Project

## Introduction

Welcome to the **URL Shortener** project! This is a simple web application built with FastAPI and Jinja2 templates, allowing users to shorten long URLs into short, easy-to-share links. The project also includes a feature to redirect users from the shortened URL to the original URL.

The application is designed with a focus on simplicity and ease of use, and it provides a great example of how to integrate FastAPI with a relational database using SQLAlchemy, and how to render dynamic HTML templates using Jinja2.

## Features

- **URL Shortening:** Convert long URLs into shorter versions.
- **Redirection:** Redirect users from a short URL to the original long URL.
- **User-Friendly Interface:** A clean and simple web interface built with HTML and styled using CSS.

## Prerequisites

Before running this project, ensure you have the following installed on your system:

- **Python 3.7+**
- **pip** (Python package manager)

## Setup Instructions

Follow these steps to get the project up and running on your local machine:

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

### 2. Install Required Libraries

Navigate to the project directory and install the required Python libraries:
```bash
pip install fastapi sqlalchemy jinja2 uvicorn psycopg2-binary
```

### 3. Project Structure
Ensure your project structure looks like this:

```
your_project/
│
├── main.py
├── templates/
│   ├── index.html
│   └── result.html
└── static/
    └── styles.css
```

### 4. Configure the Database
This project uses NeonDB (PostgreSQL) as its database. Update the connection string in the main.py file under SQLALCHEMY_DATABASE_URL with your NeonDB credentials:
```
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@hostname/database_name?sslmode=require"

```

### 5. Run the Server
Start the FastAPI server by running the following command:
```
uvicorn main:app --reload

```
This will start the server on http://localhost:8000. Open this URL in your web browser to access the application.
### 6. Usage
- **Shorten a URL** : Go to the home page, enter a long URL, and click "Shorten URL". The application will generate a shortened URL for you.
- **Redirection** : Use the shortened URL in your browser, and it will redirect you to the original URL.
