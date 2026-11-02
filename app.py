import logging
import os
import secrets
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, url_for

from MyMcdAPI import MyMcdAPI, Role

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("mcd-ct-view")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

# --- THREAD-SAFE CACHE ---
_cache_lock = threading.Lock()
CACHE: Dict[str, Any] = {
    "date": None,
    "data": [],
    "restaurant_code": None,
    "last_update": None
}

EMAIL = os.environ.get("MCD_EMAIL", "")
PASSWORD = os.environ.get("MCD_PASSWORD", "")


# --- CORE REFRESH LOGIC ---
def _process_employee_row(api: MyMcdAPI, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Helper to process a single floorplan row and fetch employee verifications if applicable."""
    info = row.get("employeeInfo") or {}
    pos_id = info.get("position")

    # Preserve original position filter (pos_id in [1, 2])
    if pos_id not in (1, 2):
        return None

    shift = row.get("shiftPlan") or {}
    intervals = shift.get("intervals")
    if not intervals:
        return None

    full_start = intervals[0]["from"]
    full_end = intervals[0]["to"]

    start_display = full_start.split(" ")[1][:5]
    end_display = full_end.split(" ")[1][:5]

    employee_id = info.get("id")
    if not employee_id:
        return None

    try:
        verif_data = api.get_profile_verifications(employee_id)
        all_verifs = verif_data.get("verifications", [])
    except Exception as e:
        logger.warning(f"Error fetching verifications for employee {employee_id}: {e}")
        return None

    issues = []
    now = datetime.now()

    for v in all_verifs:
        # Preserve original logic: only include verifications with a defined plan
        if v.get("plan") is not None:
            status = v.get("status", "")
            is_urgent = False

            if not v.get("is_verified"):
                is_urgent = True
            elif v.get("next_verification_date") and v.get("next_verification_date") != "N/A":
                try:
                    due_date = datetime.strptime(v.get("next_verification_date"), "%d.%m.%Y")
                    days_left = (due_date - now).days
                    if days_left <= 30:
                        is_urgent = True
                except (ValueError, TypeError):
                    pass

            if is_urgent:
                issues.append({
                    "name": v.get("name"),
                    "next_date": v.get("next_verification_date"),
                    "status": status
                })

    if issues:
        return {
            "id": employee_id,
            "name": info.get("fullName", "Neznámý"),
            "shift": f"{start_display} - {end_display}",
            "start_time": start_display,
            "start_full": full_start,
            "end_full": full_end,
            "issues": issues
        }

    return None


def fetch_fresh_data() -> None:
    """Fetch floorplan and compute urgent verification statuses for all employees on shift."""
    logger.info("--- STARTING DATA REFRESH ---")

    if not EMAIL or not PASSWORD:
        raise ValueError("MCD_EMAIL and MCD_PASSWORD must be configured in environment.")

    api = MyMcdAPI(EMAIL, PASSWORD)
    api.login()
    logger.info(f"Logged in successfully as {api.role.name} for restaurant {api.restaurant_id}")

    code = api.restaurant_code
    if not code:
        logger.error("Could not find restaurant code.")
        return

    today = datetime.now().strftime("%Y-%m-%d")

    if api.role < Role.MANAGER:
        logger.error("Access level is too low to fetch whole restaurant floorplan.")
        return

    floorplan = api.get_restaurant_floorplan(today)
    rows_to_check: List[Dict[str, Any]] = []

    for group in (floorplan.get("positionGroups") or []):
        for row in (group.get("rows") or []):
            info = row.get("employeeInfo") or {}
            if info.get("position") in (1, 2):
                rows_to_check.append(row)

    results: List[Dict[str, Any]] = []

    # Process employees concurrently for fast response times
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(_process_employee_row, api, row) for row in rows_to_check]
        for future in as_completed(futures):
            res = future.result()
            if res:
                results.append(res)

    results.sort(key=lambda x: x["start_time"])

    with _cache_lock:
        CACHE["restaurant_code"] = code
        CACHE["data"] = results
        CACHE["date"] = today
        CACHE["last_update"] = datetime.now().strftime("%H:%M:%S")

    logger.info(f"--- REFRESH COMPLETE: Found {len(results)} employees with verification issues ---")


# --- ROUTES ---

@app.route("/")
def index():
    today_str = datetime.now().strftime("%Y-%m-%d")

    with _cache_lock:
        needs_refresh = (CACHE["date"] != today_str)

    if needs_refresh:
        try:
            fetch_fresh_data()
        except Exception as e:
            logger.error(f"Error fetching data on load: {e}")
            flash(f"Chyba při načítání dat: {str(e)}", "danger")

    with _cache_lock:
        return render_template(
            "index.html",
            employees=CACHE["data"],
            restaurant_code=CACHE["restaurant_code"],
            last_update=CACHE["last_update"],
            cache_date=CACHE["date"]
        )


@app.route("/refresh")
def force_refresh():
    try:
        fetch_fresh_data()
        flash("Data byla úspěšně synchronizována!", "success")
    except Exception as e:
        logger.error(f"Error during manual refresh: {e}")
        flash(f"Chyba při synchronizaci: {str(e)}", "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
