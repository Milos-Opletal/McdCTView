# McdCTView

A web-based verification monitoring dashboard for McDonald's restaurants in the Czech Republic and Slovakia. It inspects today's scheduled floorplan to identify crew members with unverified stations or training certifications expiring within 30 days, enabling managers and Crew Trainers to take action during active shifts.

---

## Features

- **Daily Floorplan Sync**: Fetches scheduled restaurant shifts and floorplan allocations directly from `mymcd.eu`.
- **Verification Auditing**: Concurrently evaluates training certifications across all staff on shift.
- **Shift Status Indicators**: Dynamically highlights employees currently working, dims upcoming shifts, and hides ended shifts.
- **Configurable Restaurant Targeting**: Automatically resolves the manager's primary restaurant or targets a specific location via environment variables.
- **Department Filtering**: Instant filtering for Kitchen vs. Service stations.

---

## Tech Stack

- **Backend**: Python 3.10+ / Flask, served with Gunicorn
- **Frontend**: Jinja2 templates, Bootstrap 5, Bootstrap Icons, Montserrat typography
- **API Client**: [MyMcdAPI](https://github.com/Milos-Opletal/MyMcdAPI)
- **Deployment**: Docker & Docker Compose

---

## Prerequisites

- **Python 3.10+** (for local development)
- **Docker & Docker Compose** (for container deployment)
- A **MyMcd.eu** account with at least **Manager** level access

---

## Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

```env
# Required: McDonald's API credentials (Manager role required)
MYMCD_EMAIL=your_email@example.com
MYMCD_PASSWORD=your_password_here

# Optional: Specific restaurant override (auto-detected from your account if omitted)
# MYMCD_RESTAURANT_ID=18
# MYMCD_RESTAURANT_CODE=CZ018

# Optional: Persistent secret key for Flask sessions
FLASK_SECRET_KEY=generate_a_random_secret_key_here
```

---

## Running Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the development server
python app.py
```

The application will be accessible at `http://localhost:5000`.

---

## Deployment with Docker

```bash
docker compose up -d --build
```

### Container Configuration

| Parameter | Value |
|-----------|-------|
| Container Name | `mcd-verification-monitor` |
| Image Name | `mcd-verification-monitor` |
| Internal Port | `8000` |
| Host Port | `4332` |
| Network | `nginx_default` (external) |
| Environment Variables | `MYMCD_EMAIL`, `MYMCD_PASSWORD`, `MYMCD_RESTAURANT_ID`, `MYMCD_RESTAURANT_CODE`, `FLASK_SECRET_KEY` |

---

## Usage

- **Automatic Refresh**: Data refreshes automatically on the first visit of each day and is cached in memory.
- **Manual Refresh**: Click **Obnovit data** to perform a real-time sync with `mymcd.eu`.
- **Department Filters**: Toggle between Kitchen and Service station views.
- **On-Shift Filter**: Filter to only show employees currently working on shift.

---

## Disclaimer

This project is an independent tool developed for shift synchronization and operational analytics. It is not affiliated with, endorsed by, or sponsored by McDonald's Corporation.
