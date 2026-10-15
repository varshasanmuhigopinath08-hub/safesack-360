# SafeSack 360

**Every bag has a story. Every worker deserves a warning.**

Hazard detection and chain-of-custody for informal waste recyclers. SafeSack 360 finds hazardous items in dry-waste bags *before* a worker's hand does, labels every bag with a unique QR, and warns the next person in the chain in **English, Tamil or Hindi**, in text and in voice.

Built by **Team Twin Titans** (Sahana S, Varsha Sanmuhi G) for a 12-hour hackathon.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Flask](https://img.shields.io/badge/Flask-backend-black) ![SQLite](https://img.shields.io/badge/SQLite-database-lightgrey) ![Languages](https://img.shields.io/badge/UI-EN%20%7C%20TA%20%7C%20HI-green)

---

## The problem

Informal waste recyclers face severe occupational hazard exposure because hazardous materials (batteries, sharps, broken glass, chemicals) are mixed, unlabeled, into dry municipal waste bags. Workers cannot know what is inside before they reach in, so cuts, chemical exposure and fires follow, and nobody in the chain has a shared record of what a bag contains.

## Our solution

One chain with six checkpoints:

1. **Register** the bag (bag ID, zone) behind a **no-touch PPE gate**.
2. **Open and capture:** the bag is opened with tongs, never by hand. A camera above the conveyor belt takes **timed photos**.
3. **Detect:** AI identifies items and hazard classes with **confidence scores**.
4. **Label:** a unique **QR code** with a risk colour is generated and pasted on the bag.
5. **Scan and alert:** the disposer scans the QR, sees the alerts and hears a **voice alert** in their language.
6. **Dispose:** items are segregated, the QR is deleted or disabled, and certified disposal is logged.

Low-confidence detections go to **human review**, and the bag stays high-risk until cleared. Bags that arrive with no label follow the **Unknown Bag Protocol**.

## Three portals

| Portal | Who | What they do |
|---|---|---|
| **Collector** | Waste collectors | Register bags, PPE and no-touch checklist, conveyor station (timed photos), AI results and review, QR label, report unlabeled bags, near-miss and hazard reports |
| **Disposer** | Disposal staff | Scan QR, hazard alerts with procedures, voice alerts (EN/TA/HI), segregation checklist, **delete or disable QR**, certified disposal |
| **Admin** | Supervisors | User and employee management, hazards by date, hotspot zones, live coordination gaps, audit trail, data retention, AI model evaluation, CSV exports |

## Features

- No-touch policy enforced by a PPE gate before the camera station unlocks
- Timed photo capture from webcam, phone camera, simulated belt, or multi-upload
- Hazard classes with confidence scores, severity, and per-class pickup, container and disposal procedures
- Needs Review queue for detections below 70% confidence
- Unique QR per bag with printable label and reprint (reason logged)
- Voice alerts and a fully switchable UI in **English, தமிழ், हिन्दी**
- QR **delete** (retired from scans, audit record kept) or **disable** (reversible)
- Full chain-of-custody timeline per bag
- Coordination gaps: bags not received in time, unresolved reviews, unverified bags, hazard-heavy zones
- Audit trail and login history, with logs retained for **at least 15 days**
- Evaluation of detection accuracy, response time and service effectiveness

## How it is evaluated

| Measure | How |
|---|---|
| Detection accuracy | Accuracy, precision, recall and confusion matrix on held-out images (admin **AI Model Eval** page) |
| Response time | Capture-to-alert and label-to-receipt time recorded for every bag |
| Service effectiveness | Hazards caught before disposal, bags verified, coordination gaps closed, average time to disposal |

## Tech stack

Python and Flask, SQLite, HTML/CSS/JavaScript (Tailwind via CDN), Chart.js, `qrcode` and Pillow for QR labels, `gTTS` for pre-generated multilingual voice alerts, and an on-device vision model for detection (no cloud AI API or API key required).

## Getting started

**Requirements:** Python 3.10+, Chrome, a webcam (or use the built-in simulation mode).

```bash
# 1. Clone
git clone https://github.com/<your-username>/safesack-360.git
cd safesack-360

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
copy .env.example .env         # Windows  (cp .env.example .env on macOS / Linux)

# 5. Create and seed the database
python seed.py
python seed_demo.py            # optional: simulated demo data

# 6. Generate voice alerts (needs internet, one time)
python scripts/generate_audio.py

# 7. Run
python app.py
```

Open **http://localhost:5000**.

### Demo logins

| Role | Employee ID | Password |
|---|---|---|
| Admin | `EMP001` | `demo123` |
| Collector | `EMP101` | `demo123` |
| Disposer | `EMP201` | `demo123` |

These are demo credentials only. Change them before any real use.

### Configuration (`.env`)

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Flask session secret |
| `RETENTION_DAYS` | Log retention, minimum 15 |
| `DEMO_MODE` | `1` uses the simulation and fallback paths |

## Camera options

| Mode | Use |
|---|---|
| Laptop webcam | Default conveyor station camera |
| Phone IP camera | Phone camera over the same Wi-Fi |
| Simulation | Images from `demo_images/` fed on a timer, with an animated belt |
| Multi-upload | Select several photos at once |

In a real deployment the camera is mounted above the conveyor belt. The prototype uses a laptop webcam to simulate it.

## Project structure

```
safesack-360/
├── app.py
├── db.py
├── schema.sql
├── seed.py
├── seed_demo.py
├── requirements.txt
├── .env.example
├── blueprints/        # auth, collector, disposer, admin
├── services/
├── scripts/           # generate_audio.py
├── templates/
├── static/            # css, js, i18n (en, ta, hi), audio, qr, model
├── demo_images/
├── eval_set/
└── docs/screenshots/
```

## Screenshots

| Admin dashboard | Certified disposal |
|---|---|
| ![Admin dashboard](docs/screenshots/admin-dashboard.png) | ![Certified disposal](docs/screenshots/certified-disposal.png) |

## Limitations (honest by design)

- A camera cannot see inside a sealed bag, so SafeSack 360 photographs **opened** bags on a conveyor and never claims to see through opaque bags.
- The model recognises only the hazard classes it was trained on. Anything below 70% confidence is sent to human review rather than guessed.
- A QR label records what was detected and declared. It is a safety aid, not proof that a bag is hazard-free.
- Dashboard figures seeded by `seed_demo.py` are simulated demonstration data.
- Procedures are practical guidance and should be checked against local waste-management regulations before real deployment.

## Roadmap

- Real conveyor camera integration
- More hazard classes and a larger training set
- SMS and WhatsApp alerts to coordinators
- Offline-first mobile app for collectors
- Hotspot map view by ward

## Team

**Twin Titans**

- Sahana S
- Varsha Sanmuhi G

## License

Released under the MIT License. See `LICENSE`.
