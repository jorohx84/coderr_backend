Project Description

Coderr is a comprehensive freelancer platform designed specifically for developers. The platform connects service providers (developers) with clients looking for various development services. Developers can create and publish offers with different pricing models—Basic, Standard, and Premium—tailored to meet diverse client needs.
Clients can browse through these offers, place orders, and ultimately benefit from a transparent and flexible marketplace. Additionally, the platform allows clients to rate and review the services they receive, ensuring quality feedback and fostering trust between developers and clients.
Coderr aims to streamline the collaboration between freelancers and clients by providing all essential backend functionalities to support a seamless user experience.

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
