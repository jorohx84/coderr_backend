Project Description

Coderr is the backend for a freelancer developer platform. Your frontend teammates have already built the frontend interface. Your task is to develop the backend with all necessary functionalities to power the platform and connect frontend and backend seamlessly.
This backend handles user management, offers, orders, reviews, and more, providing a robust API for the frontend to consume.

Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
Python 3.8+
pip
virtualenv (optional but recommended)
PostgreSQL (or another database configured in your settings)
Node.js and npm (only needed if you want to run the frontend locally)

Installation (Quick Start)

Clone the repository

git clone https://github.com/yourusername/coderr-backend.git
cd coderr-backend


Create and activate a virtual environment

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


Install dependencies

pip install -r requirements.txt


Apply database migrations

python manage.py migrate


Run the development server

python manage.py runserver
