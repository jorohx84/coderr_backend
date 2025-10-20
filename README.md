# Coderr - Freelancer Platform for Developers

Coderr is a comprehensive freelancer platform designed specifically for developers. The platform connects service providers (developers) with clients looking for various development services.

Developers can create and publish offers with different pricing models — **Basic**, **Standard**, and **Premium** — tailored to meet diverse client needs. Clients can browse through these offers, place orders, and benefit from a transparent and flexible marketplace.

Additionally, the platform allows clients to **rate and review** the services they receive, ensuring quality feedback and fostering trust between developers and clients.

> Coderr aims to streamline the collaboration between freelancers and clients by providing all essential backend functionalities to support a seamless user experience.

---

## 🚀 Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

---

### ✅ Prerequisites

Make sure the following are installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (optional but recommended)
- [PostgreSQL](https://www.postgresql.org/) (or any database you configured in `settings.py`)
- [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) (only needed if you want to run the frontend locally)

---

### ⚙️ Installation (Quick Start)

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/coderr-backend.git
```


#### 2. Create and activate a virtual environment

##### Linux/MacOS:

```bash
python -m venv env
```

```bash
source env/bin/activate
```
#### Windows:

```bash
python -m venv env
```

```bash
env/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```


