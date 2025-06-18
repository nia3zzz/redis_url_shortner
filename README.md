# Redis URL Shortener

## Overview

Backend service for a learning project of a **URL shortening app**, built with **FastAPI** and **Redis**. It provides fast redirection, generates unique short codes for long URLs, and uses Redis to store the mappings.

## Tech Stack

- **Python** (FastAPI)
- **Redis**
- **Uvicorn**
- **Pydantic**
- **dotenv**

## Installation

### Clone Repository

```bash
git clone https://github.com/nia3zzz/redis_url_shortner
cd redis_url_shortner
```

### Install Dependencies

(Optional but recommended) Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install dependencies from the provided dependecy file:

```bash
pip install -r requirements.txt
```

### Setup Environment Variables

Copy the sample environment file:

```bash
cp .env.sample .env
```

### Run Redis Server

Ensure Redis is running on your machine:

```bash
redis-server
```

### Start the Server

```bash
fastapi run dev
```

The server will start at `http://localhost:8000`

## Usage

- **Base API URL**: `http://localhost:8000`
