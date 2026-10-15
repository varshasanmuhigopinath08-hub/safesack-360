# SafeSack 360 — 5-Minute Live Demo & Walkthrough Script

> **SafeSack 360** is an offline-capable, client-side hazard-detection and chain-of-custody tracking platform built to protect informal waste workers handling municipal dry waste bags.

---

## ⚡ Quick Setup & Credentials

- **Server URL**: `http://localhost:5000` (or `http://127.0.0.1:5000`)
- **Default Password**: `demo123`
- **Demo Accounts**:
  - **Administrator**: `EMP001`
  - **Field Collectors**: `EMP101` (Zone-A), `EMP102` (Zone-B)
  - **Facility Disposer**: `EMP201` (Disposal Facility)

---

## ⏱️ 5-Minute Timed Walkthrough

### Minute 1: Executive Operations & Hazard Hotspots (Role: Admin)
1. **Login**: Navigate to `http://localhost:5000` and log in as `EMP001` / `demo123`.
2. **Dashboard Overview**:
   - Point out the **6 Executive KPI Metric Cards**: Total Tracked Bags, Hazardous Bags, Needs AI Review, Open Incidents, Bags Disposed, and Average Transit Response Time.
   - Point out the **15-Day Stacked Hazard Chart** (Chart.js) breaking down hazards across battery, sharps, glass, lamp CFL, chemical, aerosol, and e-waste.
   - View the **Per-Zone Hotspot View** showing hazard density across `Zone-A` through `Zone-D`.
3. **Language Switcher**: Click **தமிழ்** (Tamil) and **हिन्दी** (Hindi) in the top right to show instant UI localization without page reloads.

---

### Minute 2: Field Intake & No-Touch AI Conveyor Station (Role: Collector)
1. **Switch Role**: Log out and log in as field collector `EMP101` / `demo123`.
2. **Register Bag**:
   - Click **"Register Bag"**, select `Zone-A`, and enter source notes (e.g. `Commercial Sector 4 route`).
   - Click **"Register Waste Sack"** &rarr; Generates unique code (e.g. `SS1026`) and cryptographic QR token.
3. **No-Touch PPE Safety Gate**:
   - Show the mandatory safety banner: Attempting to bypass shows an error.
   - Check all 5 safety requirements (no bare hands, heavy gauntlets, mask, cutter/tongs ready, clear area).
   - Click **"Confirm PPE & Unlock Station"**.
4. **Conveyor Inspection**:
   - On the Station page, demonstrate the mode switcher:
     - **Webcam**: Live camera preview with device dropdown (supports Iriun/DroidCam phone webcam).
     - **Simulation Mode**: Click **"Simulation"** to see sample waste items move along the animated CSS conveyor belt.
   - Click **"Start Conveyor Scan"**: Watch the countdown timer, capture flash, and live thumbnail gallery.
   - Point out client-side inference: **No external API keys or cloud AI services used**; TensorFlow.js classifies directly in the browser.
5. **Results & Label Generation**:
   - Click **"Review Analysis Results"**: Review hazard classifications, severity tags, and confidence scores.
   - Click **"Generate QR & Print Label"**: View the printable custody tag containing hazard symbols, emergency handling instructions, and high-contrast QR tag.

---

### Minute 3: Dock Receiving, Multilingual Voice Alert & Segregation (Role: Disposer)
1. **Switch Role**: Log in as facility disposer `EMP201` / `demo123`.
2. **Scan Inbound Sack Label**:
   - Click **"Scan QR Label"** (opens HTML5 camera scanner with manual fallback input).
   - Type in the bag code (e.g. `SS1023` or your newly created bag) and click **"Confirm Inbound Receipt"**.
   - Notice the status updates to `received`, and transit time is recorded.
3. **Multilingual Safety Voice Alert**:
   - The bag detail page automatically triggers the voice alert for the bag's highest hazard in the active language (e.g. *"Warning. This bag contains batteries. Do not mix with regular dry waste..."*).
   - Demonstrate the **Replay Voice Alert** button, **Mute Toggle**, and click-to-play fallback for autoplay-restricted browsers.
4. **Hazard Segregation Checklist**:
   - Sorters use safety tongs to transfer hazardous items into color-coded bins. Check off each item in the **Segregation Checklist**.
   - Notice the **"Complete Disposal"** button unlocks only when all hazardous items are checked.
5. **Certified Final Disposal**:
   - Click **"Complete Disposal & Close Custody"**.
   - In the modal, explain the QR policy:
     - **Delete QR Tag (Default)**: Retires QR code from future scans while preserving the database audit record.
     - **Disable QR Tag**: Temporarily freezes QR code.
   - Confirm disposal &rarr; Bag status becomes `disposed` and event is timestamped.

---

### Minute 4: Live Coordination Gaps & Operational Safety Gaps (Role: Admin)
1. **Log in as Admin** (`EMP001`).
2. **Navigate to "Incidents & Gaps"**:
   - Show the live **Coordination Gaps** panel computed in real-time:
     - **Delayed Transit Alerts**: Points out bags labelled in the field that haven't arrived at the sorting dock within the allowed time (demonstrates `SS1023`, `SS1024`, `SS1025` from the seed script).
     - **Unresolved AI Reviews**: Bags with confidence $< 70\%$ flagged for supervisor inspection.
     - **Quarantine Holds**: Unlabeled bags registered under Unknown Bag Protocol.
     - **Zone Hotspots**: Clusters of 3+ hazardous bags within 24 hours.
   - Demonstrate adjusting the **Transit Alert Threshold** (e.g., from `10` to `5` minutes) &rarr; Observe the alerts update immediately.

---

### Minute 5: In-Browser AI Model Evaluation & Effectiveness Metrics (Role: Admin)
1. **Navigate to "AI Eval"** (`/admin/evaluation`).
2. **Run Benchmark**:
   - Click **"Run In-Browser AI Evaluation"**.
   - Observe live progress as the client-side TensorFlow.js model loads `eval_set/labels.csv` and classifies each benchmark image.
3. **Review Evaluation Analytics**:
   - **Overall Accuracy**: Typically $>90\%$.
   - **Per-Class Precision, Recall, and F1 Table**: Shows performance for each hazard class.
   - **Confusion Matrix**: Full ground truth vs. predicted classification matrix with color-coded diagonal.
   - **Unrecognised Rate**: Reports percentage of low-confidence items ($<0.70$) isolated for manual review.
4. **Service Effectiveness Telemetry**:
   - Explain the labeled metrics:
     - **Capture &rarr; Alert Latency** (`~215 ms`) &rarr; **[Measured in Operations]**
     - **Share of Bags Verified** (`>90%`) &rarr; **[Measured Operational Data]**
     - **Hazards Caught Pre-Disposal** (`>95%`) &rarr; **[Measured vs Sorter Feedback]**
     - **Avg Time to Disposal** (`~24 min`) &rarr; **[Simulated Operational Pipeline]**
   - Note how the new evaluation run is immediately saved to the **Historical Benchmark Validation Runs** table and database audit trail.

---

## 🛠️ Troubleshooting Guide

### 1. Camera Busy or Permission Denied
- **Symptoms**: Video box shows "Camera denied or busy" or black screen.
- **Root Cause**: Another application (Zoom, Teams, Chrome tab) is holding the webcam lock, or browser permissions were declined.
- **Resolution**:
  1. On the Conveyor Station page, click the **"Simulation"** tab to run the full inspection workflow using high-contrast simulated waste items.
  2. Or click the **"Multi-Upload"** tab to select photos from disk.
  3. To reset permissions in Chrome: Click the lock icon in the address bar &rarr; **Site settings** &rarr; **Camera** &rarr; **Allow**.

### 2. Browser Audio Autoplay Blocked
- **Symptoms**: Voice alert does not sound automatically on entering the bag detail page.
- **Root Cause**: Modern browsers (Chrome, Edge, Safari) block unmuted audio until the user has interacted with the page.
- **Resolution**:
  - Click the prominent **"▶ Play Voice Alert (Browser Autoplay Paused)"** or **"Replay Voice Alert"** button.
  - The system will play the pre-generated MP3 or smoothly fall back to the browser's built-in `window.speechSynthesis` API.

### 3. QR Code Won't Scan on Physical Camera
- **Symptoms**: The camera scanner struggles with glare, low lighting, or crumpled paper.
- **Resolution**:
  - Use the built-in **Manual Identifier Entry** fallback directly beneath the scanner on the Receive Bag page.
  - Type the bag code (e.g. `SS1002`) and click **"Confirm Inbound Receipt"**.

### 4. Offline or Slow Network
- **Symptoms**: CDNs take longer to load on low-bandwidth field connections.
- **Resolution**:
  - The Teachable Machine TensorFlow.js model files (`model.json`, `metadata.json`, weights) are stored locally in `/static/model/` and cached by the browser.
  - If TensorFlow.js fails to initialize, the Conveyor Station automatically activates **Fallback / Manual Mode**, allowing workers to classify items via keywords or buttons.

---

## 📋 Verification & Safety Audit Notes
- **Data Protection Policy**: Bags and hazard detections are permanently preserved in SQLite and are strictly protected from deletion under the Data Retention Policy (`MIN_RETENTION_DAYS = 15`).
- **Platform Subprocess Note**: On Windows environments with restricted process spawning, all seed routines, audio generation, and retention compliance checks run safely within the native Flask process upon file save/reload without requiring external shell executions.
