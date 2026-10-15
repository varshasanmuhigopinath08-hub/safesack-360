# SafeSack 360 — Presentation Deck
## Team: Twin Titans
**Team Members:** Sahana S, Varsha Sanmuhi G  
**Project:** SafeSack 360 (Hazard-Detection & Chain-of-Custody System for Informal Waste Workers)

---

## Slide 1: Title & Overview

- **Slide Title**: SafeSack 360: AI-Powered Hazard Detection & Chain-of-Custody Tracking
- **Subtitle**: Protecting Informal Waste Workers with Edge AI Safety & Traceability
- **Team Name**: **Twin Titans**
- **Team Members**: **Sahana S**, **Varsha Sanmuhi G**
- **Domain**: Occupational Health & Safety / Municipal Waste Management / Edge Computer Vision

### Key Talking Points:
- Informal waste workers handle hundreds of tons of municipal dry waste daily under dangerous, unmonitored conditions.
- SafeSack 360 introduces an end-to-end digital and physical chain of custody with client-side AI hazard detection.
- Built specifically for ground reality: offline-capable, zero cloud API costs, and voice-guided in regional vernacular languages (English, Tamil, Hindi).

### 📸 Screenshot Needed for Slide 1:
- **Screenshot 1A**: SafeSack 360 Login Portal or Main Brand Welcome Banner showing English/Tamil/Hindi language options and role selectors (`/login`).

---

## Slide 2: Problem Statement & Field Challenges

- **Slide Title**: The Hidden Hazards of Municipal Dry Waste
- **Subtitle**: High Occupational Risk with Zero Traceability

### Core Problems:
1. **Severe Physical Hazards**:
   - Puncture wounds from unshielded hypodermic syringes and surgical sharps.
   - Deep lacerations from shattered glass and fluorescent CFL bulbs (toxic mercury vapour exposure).
   - Explosion and fire risks from damaged lithium-ion batteries and aerosol cans in collection trucks.
2. **The "Blind Transfer" Dilemma**:
   - Once waste sacks leave households or commercial zones, downstream sorting facility workers have zero visibility into sack contents until they reach inside with bare hands.
3. **Language & Literacy Barriers**:
   - The majority of informal waste pickers and sorters communicate in local vernacular languages (Tamil, Hindi) and cannot read technical safety data sheets.
4. **Coordination & Transit Gaps**:
   - Sacks delayed or lost in transit between collection and disposal create hazardous decomposition and accountability voids.

### 📸 Screenshot / Visual Needed for Slide 2:
- **Screenshot 2A**: Incident & Coordination Gaps Log showing real-world hazard categories (Needle puncture, battery thermal event, unlabeled sack) from `/admin/incidents`.

---

## Slide 3: Proposed Solution & System Architecture

- **Slide Title**: SafeSack 360: End-to-End Safety Pipeline
- **Subtitle**: Edge Computer Vision + Cryptographic QR Custody + Vernacular Voice Alerts

### The 4-Pillar Safety Architecture:
1. **No-Touch PPE Safety Gate**: Mandatory physical verification protocol preventing manual sack opening without puncture-proof gauntlets, tongs, and eye protection.
2. **100% Client-Side Edge AI**: Teachable Machine TensorFlow.js runs completely within the browser. Zero cloud AI costs, zero external network dependency, and sub-300ms inference time.
3. **Cryptographic QR Custody Tracking**: High-contrast printable labels linking physical sacks to digital custody timelines, hazard severity ratings, and GPS/zone origins.
4. **Vernacular Voice Guidance**: Pre-synthesized acoustic audio alerts in English, Tamil, and Hindi that automatically warn sorters of the bag's highest hazard class upon arrival.

### System Workflow:
```
[Bag Registration] ➔ [No-Touch PPE Check] ➔ [Conveyor AI Scan] ➔ [QR Label Print]
                                                                        │
[Certified Disposal] 🠤 [Tongs Segregation] 🠤 [Voice Warning] 🠤 [Dock QR Scan]
```

### 📸 Screenshot / Visual Needed for Slide 3:
- **Diagram / Screenshot 3A**: System architecture diagram or full custody journey timeline from `/admin/bags` or `/disposer/bag/<id>`.

---

## Slide 4: Collector Portal & AI Conveyor Inspection

- **Slide Title**: Collector Experience: Zero-Touch Intake & In-Browser AI
- **Subtitle**: AI Classification directly at the Collection Dock

### Key Features:
- **5-Point Mandatory PPE Verification**: Digital safety gate ensuring collector confirms gloves, tongs, mask, and cutter before conveyor unlocks.
- **Multi-Mode Conveyor Station**:
  - Live Webcam with camera device switcher (supports phone-as-webcam).
  - Simulated Conveyor Belt with animated preview and high-contrast demo items.
  - Multi-photo upload for field cameras.
- **In-Browser Classification**:
  - Automatically identifies 9 classes: Battery, Sharps, Glass, CFL Lamp, Chemical, Aerosol, E-Waste, Safe Recyclable, and Empty Belt.
  - Automated confidence scoring: Items $< 70\%$ confidence trigger "Needs Review" and quarantine hold.
- **Printable Hazard Label**:
  - Encodes bag ID, cryptographic token, risk color code (Red/Amber/Green), and emergency instructions.

### 📸 Screenshots Needed for Slide 4 (Primary Prototype Screens):
- **Screenshot 4A (Essential)**: **No-Touch PPE Safety Gate Modal** with 5 checkboxes and the prominent yellow safety banner (`/collector/bag/<id>/ppe`).
- **Screenshot 4B (Essential)**: **Conveyor Station Live Scan** showing the camera/simulation preview, countdown timer, captured thumbnail strip, and live TensorFlow.js predictions (`/collector/bag/<id>/station`).
- **Screenshot 4C (Optional/Recommended)**: **Printable Hazard QR Label View** showing the printable custody tag with hazard symbols (`/collector/bag/<id>/label`).

---

## Slide 5: Disposer Portal, Vernacular Voice Alerts & Safe Segregation

- **Slide Title**: Disposer Experience: Acoustic Warnings & Safe Containment
- **Subtitle**: Voice-First Hazard Awareness & Certified QR Disposal

### Key Features:
- **Instant Inbound Receiving**:
  - In-browser HTML5 camera QR scanner or fast bag-code lookup.
  - Real-time transit response time calculation (`labelled_at` ➔ `received_at`).
- **Autoplay Multilingual Voice Alert**:
  - Speaks immediately in the worker's chosen language:
    - *Tamil*: "எச்சரிக்கை. இந்த பையில் பேட்டரிகள் உள்ளன. தீ மற்றும் இரசாயன ஆபத்து..."
    - *Hindi*: "चेतावनी। इस बैग में बैटरियां हैं। आग और रासायनिक खतरा..."
    - *English*: "Warning. This bag contains batteries. Fire and chemical hazard..."
  - Triple fallback: Cached MP3 ➔ Server on-demand gTTS ➔ Browser SpeechSynthesis.
- **Hazardous Item Segregation Checklist**:
  - Interactive checklist requiring every hazardous item to be isolated into color-coded containers with safety tongs.
  - Disposal action is cryptographically blocked until all items are verified.
- **QR Retirement Policy**:
  - Disposer selects "Delete QR" (retires tag permanently while preserving audit log) or "Disable QR".

### 📸 Screenshots Needed for Slide 5 (Primary Prototype Screens):
- **Screenshot 5A (Essential)**: **Disposer Bag Safety Detail Page** showing the Big RED Hazard Alert Banner, hazard items list, and the **Audio Voice Player** button (`/disposer/bag/<id>`).
- **Screenshot 5B (Essential)**: **Hazard Segregation Checklist & Final Disposal Modal** showing checkboxes for each hazard and the "Delete/Disable QR" confirmation dialog (`/disposer/bag/<id>`).
- **Screenshot 5C (Optional)**: **Inbound QR Scanner Screen** showing camera viewfinder and manual entry fallback (`/disposer/scan`).

---

## Slide 6: Admin Operations, Coordination Gaps & AI Evaluation

- **Slide Title**: Admin Intelligence: Hotspot Tracking & Model Telemetry
- **Subtitle**: Proactive Gap Mitigation & Client-Side Benchmarking

### Key Features:
- **Executive Operations Center**:
  - 6 Real-time KPI Cards (Total bags, hazardous ratio, open incidents, average response time).
  - 15-Day Stacked Hazard Distribution Chart (Chart.js) and Per-Zone Hotspot Density.
- **Live Coordination Gaps Engine**:
  - Automatically flags sacks in transit exceeding safety thresholds ($>10$ min).
  - Flags unresolved AI reviews and quarantine bags.
- **In-Browser AI Evaluation Engine**:
  - Runs client-side TensorFlow.js on `eval_set/labels.csv` benchmark.
  - Generates confusion matrix, per-class precision/recall, and average inference latency.
- **Service Effectiveness Metrics**:
  - Capture-to-alert latency ($<250$ ms) **[Measured]**.
  - Verified bag share ($>90\%$) **[Measured]**.
  - Hazards caught pre-disposal ($>95\%$) **[Measured]**.
- **Data Privacy & Retention**:
  - Enforced 15-day minimum retention (`MIN_RETENTION_DAYS = 15`). Audit logs purged safely while bags and detections are permanently protected.

### 📸 Screenshots Needed for Slide 6 (Primary Prototype Screens):
- **Screenshot 6A (Essential)**: **Admin Operations Dashboard** showing the KPI cards, 15-Day Hazard Chart, and Zone Hotspot Bar Chart (`/admin/dashboard`).
- **Screenshot 6B (Essential)**: **Coordination Gaps Panel** showing active delayed transit warnings (e.g. `SS1023`, `SS1024`) and threshold settings (`/admin/incidents`).
- **Screenshot 6C (Essential)**: **In-Browser AI Evaluation Page** showing the Confusion Matrix, Precision/Recall Table, and Service Effectiveness cards (`/admin/evaluation`).

---

## Slide 7: Impact, Technical Innovations & Future Roadmap

- **Slide Title**: Real-World Impact & Technical Novelty
- **Subtitle**: Scalable, Zero-Cloud-Cost Safety for Millions of Waste Handlers

### Unique Competitive Innovations:
1. **Zero Cloud API Reliance**: Runs local TensorFlow.js inference directly in the browser; operates even in bandwidth-constrained collection points with no per-query API bills.
2. **Vernacular Acoustic Guidance**: Bridges the literacy divide for informal waste workers using natural Tamil and Hindi voice alerts.
3. **Closed-Loop Chain of Custody**: Cryptographic QR tags guarantee bags cannot be bypassed, dumped, or left untracked.
4. **Proactive Coordination Gap Detection**: Automatically detects delays and missing bags before injuries occur.

### Measurable Social & Environmental ROI:
- **Zero Preventable Needlestick & Glass Injuries** through mandatory No-Touch PPE and voice warnings.
- **Prevention of Landfill & Truck Fires** by isolating lithium-ion batteries prior to compaction.
- **Formalized Dignity of Labor** for municipal and informal waste pickers through safety technology.

### Future Roadmap:
- Smart-bin IoT integration with low-cost ESP32 camera sensors.
- Offline-first Progressive Web App (PWA) with background sync.
- Automated robotic sorter guidance via edge WebSocket telemetry.

---

## 📋 Summary of Screenshots to Upload:

Please capture and upload the following screenshots from your running app (`http://localhost:5000`):

1. **Screenshot 1**: **Conveyor Station with AI Detections** (`/collector/bag/<id>/station`)  
   *(Shows the camera/simulation, live predictions, and countdown)*
2. **Screenshot 2**: **No-Touch PPE Safety Gate** (`/collector/bag/<id>/ppe`)  
   *(Shows the mandatory 5 checkboxes and yellow warning banner)*
3. **Screenshot 3**: **Disposer Bag Safety Detail Page** (`/disposer/bag/<id>`)  
   *(Shows the Red/Amber hazard alert banner and voice audio guide)*
4. **Screenshot 4**: **Hazard Segregation Checklist & Disposal Modal** (`/disposer/bag/<id>`)  
   *(Shows the check-off list and Complete Disposal modal)*
5. **Screenshot 5**: **Admin Operations Dashboard & Hotspot Charts** (`/admin/dashboard`)  
   *(Shows KPI cards and the two Chart.js visual graphs)*
6. **Screenshot 6**: **AI Evaluation Page with Confusion Matrix** (`/admin/evaluation`)  
   *(Shows the in-browser model benchmark, matrix, and service effectiveness)*
7. **Optional (Bonus)**: **Printable QR Hazard Label** (`/collector/bag/<id>/label`) or **Coordination Gaps Table** (`/admin/incidents`)
