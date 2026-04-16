# McdCTView

A Crew Trainer verification dashboard for McDonald's restaurants in the Czech Republic. It shows which employees on today's shift have missing or expiring training verifications so managers and crew trainers can act on them immediately.

**🌐 Live at [ct.mymymcd.eu](https://ct.mymymcd.eu)**

## What it does

McdCTView pulls the current day's floorplan from the MyMcd portal and cross-references each employee's training profile against the master verification list. It then displays a filterable dashboard of employees who have:

- **Unverified** training stations (not yet passed)
- **Expiring** verifications (due within 30 days)

The dashboard automatically hides employees whose shifts have already ended and visually dims those whose shifts haven't started yet. Employees can be filtered by department (Kitchen / Service) and by whether they are currently on shift.

## Tech Stack

- **Backend** — Python / Flask, served via Gunicorn
- **Frontend** — Jinja2 templates, Bootstrap 5, Bootstrap Icons
- **API** — [MyMcdAPI](https://github.com/Milos-Opletal/MyMcdAPI) — a custom wrapper used to communicate with the [mymcd.eu](https://mymcd.eu) portal
- **Deployment** — Docker / Docker Compose

## Prerequisites

- **Python 3.10+**
- **Docker** (for containerised deployment)
- A **MyMcd.eu** account with at least **Manager** level access (required to fetch the full restaurant floorplan)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Milos-Opletal/McdCTView.git
cd McdCTView
```

### 2. Create a `.env` file

```env
MCD_EMAIL=your-mymcd-email@example.com
MCD_PASSWORD=your-mymcd-password
FLASK_SECRET_KEY=some-random-secret-key
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### Running locally

```bash
python app.py
```

The app will be available at `http://localhost:5000`.

### Running with Docker

```bash
docker build -t mcd-monitor .
docker compose up -d
```

The container binds to port **4332** by default (configurable in `docker-compose.yml`).

> **Note:** The `.env` file is loaded by Docker Compose at runtime via the `env_file` directive — credentials are never baked into the image.

## Usage

- **Auto-refresh** — Data is fetched automatically on the first visit of each day and cached for the rest of the day.
- **Manual refresh** — Click the *Obnovit data* button to force a sync.
- **Filters** — Toggle *Aktuálně na směně* to show only employees currently on shift, or use the department dropdown to filter by Kitchen / Service.
- **Training profile** — Click *TRÉNINKOVÝ PROFIL* on any employee card to open their full profile on the MyMcd portal.

## License

This project is not affiliated with or endorsed by McDonald's Corporation.
