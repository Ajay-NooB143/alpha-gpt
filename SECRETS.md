# GitHub Secrets

This document lists all GitHub secrets required to run the CI/CD workflows in this repository.

To add a secret: **Settings → Secrets and variables → Actions → New repository secret**

---

## Required Secrets

### Trading / Exchange

| Secret | Description |
|--------|-------------|
| `BINANCE_API_KEY` | Binance exchange API key for placing and managing orders |
| `BINANCE_API_SECRET` | Binance exchange API secret corresponding to `BINANCE_API_KEY` |

### Notifications

| Secret | Description |
|--------|-------------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token used to send trade alerts and status messages |

### AI / LLM

| Secret | Description |
|--------|-------------|
| `OPENAI_API_KEY` | OpenAI API key used by the alpha-generation and hypothesis agents |
| `ANTHROPIC_API_KEY` | Anthropic API key (optional, used in integration tests) |

### Observability

| Secret | Description |
|--------|-------------|
| `LANGSMITH_API_KEY` | LangSmith API key for tracing LangGraph runs |

### Database

| Secret | Description |
|--------|-------------|
| `DATABASE_URL` | PostgreSQL connection string, e.g. `postgresql://user:pass@host:5432/alphagpt` |

### Deployment (deploy-bot workflow)

| Secret | Description |
|--------|-------------|
| `VPS_HOST` | Hostname or IP address of the deployment server |
| `VPS_USER` | SSH username on the deployment server |
| `VPS_SSH_KEY` | Private SSH key for authenticating with the deployment server |
| `VPS_SSH_PORT` | SSH port on the deployment server (default: `22`) |

---

## Workflow → Secret Mapping

| Workflow file | Secrets used |
|---------------|-------------|
| `trade.yml` | `BINANCE_API_KEY`, `BINANCE_API_SECRET`, `TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY`, `DATABASE_URL` |
| `trading-bot.yml` | `BINANCE_API_KEY`, `BINANCE_API_SECRET`, `TELEGRAM_BOT_TOKEN`, `DATABASE_URL` |
| `deploy-bot.yml` | `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`, `VPS_SSH_PORT` |
| `integration-tests.yml` | `ANTHROPIC_API_KEY`, `LANGSMITH_API_KEY` |
| `lint.yml` | *(none)* |
| `test.yml` | *(none)* |
| `docker.yml` | *(none)* |
| `security.yml` | *(none)* |
