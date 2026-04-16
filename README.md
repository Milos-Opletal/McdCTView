# McdCTView

A web-based dashboard for McDonald's Crew Trainers and Managers to monitor employee verification statuses during active shifts. The app connects to the [mymcd.eu](https://mymcd.eu) portal via the [MyMcdAPI](https://github.com/Milos-Opletal/MyMcdAPI) wrapper library and displays which on-shift employees have missing or expiring verifications — so you can act on them before it's too late.

## What It Does

- **Logs in** to the MyMcd portal using manager-level credentials
- **Fetches today's restaurant floorplan** to identify all employees currently scheduled
- **Checks each employee's verification status** (food safety, hospitality, station certifications, etc.)
- **Highlights urgent items** — verifications that are unverified or expiring within 30 days
- **Displays a clean, filterable dashboard** styled after the official McDonald's design, with:
  - Toggle to show only employees currently on shift vs. all scheduled today
  - Department filter (Kitchen / Service)
  - Sorting by earliest expiring verification
  - Direct links to each employee's training profile on mymcd.eu

## Prerequisites

- **Python 3.10+**
- A **MyMcd account** with **Manager-level access** (required to fetch the restaurant floorplan)
- **Docker** (optional, for containerized deployment)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Milos-Opletal/McdCTView.git
cd McdCTView
```

### 2. Create a `.env` file

```env
MCD_EMAIL=your_mymcd_email@example.com
MCD_PASSWORD=your_mymcd_password
FLASK_SECRET_KEY=any_random_secret_string
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running

### Local development

```bash
python app.py
```

The app will be available at `http://localhost:5000`.

### Docker

Build and run with Docker Compose:

```bash
docker build -t mcd-monitor .
docker compose up -d
```

The container runs via Gunicorn on port `8000`, mapped to host port `4332` by default (configurable in `docker-compose.yml`).

## MyMcdAPI

This project uses the [MyMcdAPI](https://github.com/Milos-Opletal/MyMcdAPI) library (`MyMcdAPI.py`) to interact with the mymcd.eu portal. The wrapper handles authentication, session management, and provides typed methods for endpoints such as:

- `get_restaurant_floorplan()` — today's shift layout
- `get_profile_verifications()` — training plans & verification statuses per employee
- `get_employee_shifts()` — individual shift schedules
- `get_restaurant_shifts()` — full restaurant shift data

All API methods enforce role-based access control (`CREW`, `CT`, `MANAGER`) matching the permission model of the mymcd.eu platform.

## Tech Stack

| Layer     | Technology                    |
|-----------|-------------------------------|
| Backend   | Flask, Gunicorn               |
| Frontend  | Bootstrap 5, Jinja2 templates |
| API       | MyMcdAPI (requests + BeautifulSoup) |
| Deployment| Docker, Docker Compose        |
