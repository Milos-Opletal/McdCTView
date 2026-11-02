# McdCTView

A Crew Trainer verification monitor dashboard for McDonald's restaurants in the Czech Republic and Slovakia. It automatically checks which employees on today's shift have unverified stations or training certifications expiring within 30 days so managers and Crew Trainers can take action immediately.

---

## What It Does

1. **Daily Floorplan Sync**: Fetches the restaurant floorplan for the current day from `mymcd.eu`.
2. **Verification Auditing**: Concurrently evaluates crew training status for all employees scheduled on shift.
3. **Smart Shift Filtering**: Identifies employees needing verifications, displaying their shift timing, status, and direct profile links.
4. **Live Status Tracking**: Automatically highlights on-shift employees, dims future shifts, and hides ended shifts.

---

## Tech Stack

- **Backend**: Python 3.10+ / Flask, served with Gunicorn
- **Frontend**: Jinja2 templates, Bootstrap 5, Bootstrap Icons, Montserrat typography
- **API Client**: [MyMcdAPI](https://github.com/Milos-Opletal/MyMcdAPI)
- **Deployment**: Docker / Docker Compose (compatible with Portainer)

---

## Prerequisites

- **Python 3.10+** (if running locally)
- **Docker & Docker Compose** (for containerized deployment)
- A **MyMcd.eu** account with at least **Manager** level access (required to fetch the restaurant floorplan)

---

## Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

```env
# Required McDonald's API credentials
MCD_EMAIL=your_email@example.com
MCD_PASSWORD=your_password_here

# Optional: Persistent secret key for Flask sessions
FLASK_SECRET_KEY=generate_a_random_secret_key_here
```

---

## Running Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the development server
python app.py
```

The application will be accessible at `http://localhost:5000`.

---

## Deployment with Docker / Portainer

The repository includes a production-ready `Dockerfile` and `docker-compose.yml`.

```bash
docker compose up -d --build
```

### Portainer Configuration Details

| Parameter | Value |
|-----------|-------|
| Container Name | `mcd-verification-monitor` |
| Image Name | `mcd-verification-monitor` |
| Internal Port | `8000` |
| Host Port | `4332` |
| Network | `nginx_default` (external) |
| Environment Variables | `MCD_EMAIL`, `MCD_PASSWORD` |

---

## Usage

- **Automatic Refresh**: Data refreshes automatically on the first visit of each day and is cached in memory.
- **Manual Refresh**: Click **Obnovit data** to perform a real-time sync with `mymcd.eu`.
- **Department Filters**: Filter by Kitchen / Service stations.
- **On-Shift Toggle**: Filter to only show employees currently working their scheduled shift.

---

## License

This project is an independent tool and is not affiliated with, endorsed by, or sponsored by McDonald's Corporation.
