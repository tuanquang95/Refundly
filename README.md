# Refundly

Refundly is an AI chatbot that handles return and refund requests for e-commerce stores. Customers describe what they want to send back in plain language, and Refundly checks the request against the store's return policies, explains whether the item is eligible and why, and walks the customer through the next steps.

> **Status:** early development. The API skeleton, configuration, error handling and a health check are in place. The chatbot itself is not built yet.

## What it will do

- **Chat with customers** about returns, exchanges and refunds in natural language.
- **Apply the store's policies**: return windows, item condition, non-returnable categories, proof of purchase and refund method.
- **Explain every decision** by pointing to the policy rule it is based on, so customers and support staff can see why a request was approved or declined.
- **Escalate to a human** when a request is unclear, falls outside the policies or needs an exception.
- **Plug into the store's systems** to look up orders and start the return.

## Tech stack

| Area | Tool |
| --- | --- |
| Language | Python 3.14 |
| API | [FastAPI](https://fastapi.tiangolo.com/) |
| LLM orchestration | [LangChain](https://python.langchain.com/) |
| Configuration | pydantic-settings (environment variables / `.env`) |
| Packages and environments | [uv](https://docs.astral.sh/uv/) |
| Tests and linting | pytest, Ruff |
| Deployment | Docker |

## Project structure

```
Refundly/
├── src/
│   ├── main.py            # creates the app: logging, CORS, error handlers, routers
│   ├── core/
│   │   ├── config.py      # settings
│   │   ├── logging.py     # log setup
│   │   └── exceptions.py  # AppError types and consistent JSON error responses
│   ├── api/
│   │   ├── deps.py        # shared FastAPI dependencies
│   │   └── v1/
│   │       ├── router.py  # registers every v1 endpoint under /api/v1
│   │       └── endpoints/ # one module per resource
│   ├── schemas/           # request and response models
│   └── services/          # business logic: policy checks, chatbot, LLM calls
├── tests/
├── Dockerfile
├── .env.example
└── pyproject.toml
```

## Getting started

### Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs Python 3.14 for you if you don't have it.

### Setup

```bash
uv sync                  # create .venv and install dependencies
cp .env.example .env     # then edit .env as needed
```

### Run the API

```bash
uv run fastapi dev
```

- API: http://localhost:8000/api/v1
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health

## Configuration

Settings are read from environment variables, or from a `.env` file in the project root.

| Variable | Default | Description |
| --- | --- | --- |
| `APP_NAME` | `Refundly API` | Name shown in the API docs |
| `ENVIRONMENT` | `local` | `local`, `staging` or `production`. `production` turns off `/docs`, `/redoc` and `/openapi.json` |
| `DEBUG` | `false` | FastAPI debug mode |
| `LOG_LEVEL` | `INFO` | Python log level |
| `CORS_ORIGINS` | `[]` | JSON list of allowed origins, e.g. `["http://localhost:3000"]`. CORS is off when empty |

Never commit `.env`. It is already listed in `.gitignore`.

## Development

```bash
uv run pytest                 # run tests
uv run ruff check .           # lint
uv run ruff format .          # format
uv add <package>              # add a dependency
uv add --dev <package>        # add a dev-only dependency
```

### Adding an endpoint

1. Define the request and response models in `src/schemas/`.
2. Put the logic in `src/services/`.
3. Add the route in `src/api/v1/endpoints/`.
4. Register the router in `src/api/v1/router.py`.
5. Add tests under `tests/`.

To return an error to the client, raise an `AppError` subclass from `src/core/exceptions.py`, such as `NotFoundError`. It is turned into a JSON response like this:

```json
{ "error": { "code": "not_found", "message": "Order 123 not found" } }
```

## Docker

```bash
docker build -t refundly .
docker run -p 8000:8000 --env-file .env refundly
```

The image runs as a non-root user with 4 worker processes.

## Roadmap

- [ ] Choose an LLM provider and add its LangChain integration
- [ ] Store return policies and load them into the chatbot (e.g. with retrieval, RAG)
- [ ] Chat endpoint with conversation history
- [ ] Policy eligibility checks with reasons the customer can read
- [ ] Order lookup through the store's systems
- [ ] Hand-off to a human support agent
- [ ] Authentication and rate limiting
- [ ] Database for conversations and return requests
