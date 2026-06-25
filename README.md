# ✿ JAVYRIYAH — Silent Safety Signal Protocol

A discreet safety application disguised as a standard calculator.
When a user types **1805**, it silently triggers an emergency signal,
shares their live GPS location, and notifies emergency responders.

---

## 🌸 Features

- **Disguised UI** — Looks and works like a real calculator
- **Silent Trigger** — Code `1805` activates emergency mode invisibly
- **Live GPS Tracking** — Continuous location updates sent to responders
- **Emergency Dashboard** — Authority-facing panel with real-time alerts
- **SQLite Database** — All alerts persisted with timestamps and coordinates
- **Auto-refresh** — Dashboard polls every 15 seconds for new signals
- **Google Maps Links** — Direct links to victim coordinates

---

## 🚀 Setup & Run

```bash
# 1. Navigate to project folder
cd javyriyah

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open:
- **User view (calculator):** http://localhost:5000/
- **Authority dashboard:**    http://localhost:5000/dashboard

---

## 🔐 How the Silent Signal Works

1. User opens the app — sees only a beautiful calculator
2. User types `1805` in any calculation
3. App silently:
   - Requests GPS coordinates
   - Sends POST to `/api/trigger-alert`
   - Begins continuous location tracking
   - Displays a gentle confirmation modal
4. Dashboard shows ACTIVE alert with coordinates + map link
5. Operator clicks "Resolve" once rescue is complete

---

## 📁 Project Structure

```
javyriyah/
├── app.py                  # Flask backend + SQLAlchemy models
├── requirements.txt
├── javyriyah.db            # Auto-created SQLite database
└── templates/
    ├── index.html          # Calculator UI (disguised user app)
    └── dashboard.html      # Emergency response dashboard
```

---

## ⚠️ Important Notes

- In production, **secure the `/dashboard` route with authentication**
- Consider adding **SMS/email alerts** via Twilio/SendGrid on trigger
- For deployment, use HTTPS to ensure location API works on mobile
- The secret code `1805` can be changed in `app.py` and `index.html`

---

*✿ Built with care. May it keep someone safe. ✿*
