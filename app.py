from flask import Flask, render_template, redirect, url_for, flash
from datetime import datetime
from MyMcdAPI import MyMcdAPI, Role

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# --- CACHE ---
CACHE = {
    "date": None,
    "data": [],
    "restaurant_code": None,
    "last_update": None
}

# Credentials
EMAIL = "manager@example.com"
PASSWORD = "your-password-here"


# --- CORE LOGIC ---
def fetch_fresh_data():
    print("--- STARTING DATA REFRESH ---")
    
    api = MyMcdAPI(EMAIL, PASSWORD)
    try:
        api.login()
        print(f"Logged in successfully as {api.role.name} for restaurant {api.restaurant_id}")
    except Exception as e:
        print(f"Error during API login: {e}")
        raise

    code = api.restaurant_code
    if not code:
        print("Could not find restaurant code.")
        return

    CACHE['restaurant_code'] = code

    today = datetime.now().strftime("%Y-%m-%d")
    
    try:
        if api.role >= Role.MANAGER:
            floorplan = api.get_restaurant_floorplan(today)
        else:
            print("Access level is too low to fetch whole restaurant floorplan.")
            return
    except Exception as e:
        print(f"Error fetching floorplan: {e}")
        return

    results = []

    groups = floorplan.get('positionGroups') or []
    for group in groups:
        rows = group.get('rows') or []
        for row in rows:
            info = row.get('employeeInfo') or {}
            pos_id = info.get('position')

            # User explicitly requested preserving the old `pos_id in [1, 2]` filter
            if pos_id in [1, 2]:
                shift = row.get('shiftPlan') or {}
                intervals = shift.get('intervals')
                if intervals:
                    full_start = intervals[0]['from']
                    full_end = intervals[0]['to']

                    start_display = full_start.split(' ')[1][:5]
                    end_display = full_end.split(' ')[1][:5]

                    employee_id = info.get('id')
                    
                    # Fetch verifications via the new wrapper
                    verif_data = api.get_profile_verifications(employee_id)
                    all_verifs = verif_data.get("verifications", [])
                    
                    issues = []
                    for v in all_verifs:
                        # Emulate old logic: only include ones with defined plan
                        if v.get('plan') is not None:
                            status = v.get('status', '')
                            is_urgent = False
                            
                            if not v.get('is_verified'):
                                is_urgent = True
                            elif v.get('next_verification_date') and v.get('next_verification_date') != "N/A":
                                try:
                                    due_date = datetime.strptime(v.get('next_verification_date'), "%d.%m.%Y")
                                    days_left = (due_date - datetime.now()).days
                                    if days_left <= 30:
                                        is_urgent = True
                                except:
                                    pass
                                    
                            if is_urgent:
                                issues.append({
                                    "name": v.get('name'),
                                    "next_date": v.get('next_verification_date'),
                                    "status": status
                                })

                    if issues:
                        results.append({
                            "id": employee_id,
                            "name": info.get('fullName', 'Neznámý'),
                            "shift": f"{start_display} - {end_display}",
                            "start_time": start_display,
                            "start_full": full_start,
                            "end_full": full_end,
                            "issues": issues
                        })

    results.sort(key=lambda x: x['start_time'])

    CACHE['data'] = results
    CACHE['date'] = today
    CACHE['last_update'] = datetime.now().strftime("%H:%M:%S")
    print(f"--- REFRESH DOKONČEN: Nalezeno {len(results)} zaměstnanců s verifikacemi ---")


# --- ROUTES ---

@app.route('/')
def index():
    today_str = datetime.now().strftime("%Y-%m-%d")

    if CACHE['date'] != today_str:
        try:
             fetch_fresh_data()
        except Exception as e:
             flash(f"Error fetching data on load: {str(e)}", "danger")

    return render_template('index.html',
                           employees=CACHE['data'],
                           restaurant_code=CACHE['restaurant_code'],
                           last_update=CACHE['last_update'],
                           cache_date=CACHE['date'])


@app.route('/refresh')
def force_refresh():
    try:
        fetch_fresh_data()
        flash("Data byla úspěšně synchronizována!", "success")
    except Exception as e:
        flash(f"Chyba při synchronizaci: {str(e)}", "danger")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)