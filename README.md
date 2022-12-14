# dummy stock screener

Example stock screener service.

## Features

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework for building APIs with Python.
- [SQLAlchemy](https://www.sqlalchemy.org/) - The SQL Toolkit and ORM.
- [Docker](https://docs.docker.com/) - The containerization platform.
- [Nginx](https://nginx.org/) - The web server.
- [Chart.js](https://www.chartjs.org/) - The JavaScript library for making HTML-based charts.

## Requirements

- Python 3.10
- Postgres 15.0
- Docker
- Docker Compose

## Run locally

```bash
make compose-up
make compose-restart
```

Open API docs in your browser to <http://localhost:8000/docs>  
Open screener page in your browser to <http://localhost:5000>
