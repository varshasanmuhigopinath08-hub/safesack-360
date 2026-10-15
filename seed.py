import sqlite3
import os
import uuid
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'safesack360.db')
SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')


def seed_database():
    print(f"Initializing database at: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())

    cur = conn.cursor()

    # 1. Seed Users (idempotent via employee_id UNIQUE)
    default_password_hash = generate_password_hash("demo123")
    users = [
        (
            "System Admin",
            "EMP001",
            "admin",
            "+91-9876543210",
            "Central-HQ",
            default_password_hash,
            1,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
        (
            "Murugan K",
            "EMP101",
            "collector",
            "+91-9876543211",
            "Zone-A",
            default_password_hash,
            1,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
        (
            "Ramesh Kumar",
            "EMP102",
            "collector",
            "+91-9876543212",
            "Zone-B",
            default_password_hash,
            1,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
        (
            "Priya Sharma",
            "EMP201",
            "disposer",
            "+91-9876543213",
            "Central-Facility",
            default_password_hash,
            1,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
    ]

    for u in users:
        cur.execute("""
            INSERT INTO users (name, employee_id, role, phone, zone, password_hash, active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(employee_id) DO UPDATE SET
                name=excluded.name,
                role=excluded.role,
                phone=excluded.phone,
                zone=excluded.zone,
                password_hash=excluded.password_hash,
                active=excluded.active
        """, u)
    print(f"✓ Seeded {len(users)} users.")

    # 2. Seed Hazard Classes (10 classes: battery, sharps, glass, lamp_cfl, chemical, aerosol, ewaste, biomedical, unknown, safe)
    hazard_classes = [
        (
            "battery",
            "HIGH",
            "Battery / Accumulator Cell",
            "மின்கலன் / பேட்டரி (Battery)",
            "बैटरी / सेल (Battery)",
            "Use insulated heavy-duty rubber gloves or magnetic pickup tongs. Never touch barehanded or crush casing.",
            "பாதுகாப்பான ரப்பர் கையுறைகள் அல்லது இடுக்கியைப் பயன்படுத்துங்கள். வெறும் கைகளால் தொடாதீர்கள்.",
            "इंसुलेटेड रबर दस्ताने या चिमटे का उपयोग करें। नंगे हाथों से कभी न छुएं।",
            "Rigid non-conductive plastic bin lined with dry sand with tight-sealing lid.",
            "மணல் நிரப்பப்பட்ட மின்சாரத்தை கடத்தாத கடினமான பிளாஸ்டிக் தொட்டி.",
            "रेत से युक्त गैर-प्रवाहकीय कठोर प्लास्टिक कंटेनर।",
            "Authorized e-waste battery recycling center for hydrometallurgical recovery.",
            "அங்கீகரிக்கப்பட்ட பேட்டரி மறுசுழற்சி மையத்திற்கு அனுப்பவும்.",
            "अधिकृत बैटरी पुनर्चक्रण केंद्र को सुरक्षित रूप से भेजें।"
        ),
        (
            "sharps",
            "HIGH",
            "Sharps, Needles & Blades",
            "கூர்மையான ஊசிகள் / பிளேடுகள் (Sharps)",
            "नुकीली वस्तुएं और सुइयां (Sharps)",
            "Use mechanical pickup tongs only. Never press down dry bags or grasp by bottom.",
            "நீண்ட இடுக்கியை (tongs) மட்டுமே பயன்படுத்துங்கள். ஒருபோதும் வெறும் கைகளால் தொடாதீர்கள்.",
            "केवल लंबे चिमटे (tongs) का उपयोग करें। बैग को हाथों से न दबाएं और नंगे हाथों से न छुएं।",
            "Puncture-proof rigid yellow container with tamper-evident locking lid.",
            "துளையிட முடியாத மஞ்சள் நிற கூர்மைப் பொருள் பெட்டி.",
            "पंचर-रोधी पीला शार्प्स सुरक्षा बॉक्स।",
            "Designated biohazard autoclaving and certified high-temperature incineration.",
            "அங்கீகரிக்கப்பட்ட மருத்துவக் கழிவு எரியூட்டும் பிரிவிற்கு அனுப்பவும்.",
            "अधिकृत बायोमेडिकल अपशिष्ट भस्मीकरण एवं ऑटोक्लेविंग सुविधा।"
        ),
        (
            "glass",
            "MEDIUM",
            "Broken Glass & Sharp Shards",
            "உடைந்த கண்ணாடித் துண்டுகள் (Glass)",
            "टूटा हुआ कांच और नुकीले टुकड़े (Glass)",
            "Wear level-5 cut-resistant Kevlar gloves. Pick by solid base or brush into dustpan.",
            "காயம் ஏற்படாத வெட்டு-எதிர்ப்பு கையுறைகளை அணியுங்கள். துடைப்பான் மற்றும் தட்டினால் அள்ளுங்கள்.",
            "कट-प्रतिरोधी भारी दस्ताने पहनें। ब्रश और डस्टपैन से सावधानीपूर्वक उठाएं।",
            "Double-walled corrugated cardboard box or puncture-resistant thick plastic tub.",
            "தடித்த அட்டைப் பெட்டி அல்லது வலிமையான பிளாஸ்டிக் தொட்டி.",
            "मजबूत दोहरी दीवार वाला कार्डबोर्ड बॉक्स या प्लास्टिक कंटेनर।",
            "Glass remelting and industrial cullet recycling aggregator.",
            "கண்ணாடி மறுசுழற்சி மற்றும் உருக்கும் மையத்திற்கு அனுப்பவும்.",
            "कांच गलाने एवं पुनर्चक्रण केंद्र को सौंपें।"
        ),
        (
            "lamp_cfl",
            "HIGH",
            "CFL / Fluorescent Mercury Lamp",
            "பாதரச விளக்குகள் / சி.எஃப்.எல் (CFL / Tube)",
            "सीएफएल / फ्लोरोसेंट बल्ब (CFL Lamp)",
            "Handle gently with nitrile gloves without breakage to avoid toxic mercury vapor release.",
            "உடையாமல் கவனமாகக் கையாளவும். பாதரச ஆவியை சுவாசிப்பதைத் தவிர்க்க முகக்கவசம் அணியவும்.",
            "पारे की जहरीली भाप से बचने के लिए बिना तोड़े सावधानी से उठाएं और मास्क पहनें।",
            "Padded cylindrical carton tube or dedicated shatter-proof bulb rack.",
            "மெத்தென பஞ்சு அல்லது கார்ட்போர்டு பாதுகாப்பு குழாய்.",
            "गद्देदार सुरक्षा बॉक्स या समर्पित लैंप रीसाइक्लिंग ट्यूब।",
            "Mercury reclamation facility and hazardous fluorescent dismantling unit.",
            "பாதரசம் அகற்றும் அங்கீகரிக்கப்பட்ட அபாயக் கழிவு மேலாண்மை மையம்.",
            "पारा निष्कर्षण एवं सुरक्षित फ्लोरोसेंट निपटान इकाई।"
        ),
        (
            "chemical",
            "HIGH",
            "Chemical / Solvent / Pesticide Bottle",
            "இரசாயனம் / அமிலம் / பூச்சிக்கொல்லி (Chemical)",
            "रासायनिक अपशिष्ट / कीटनाशक / एसिड (Chemical)",
            "Wear chemical-resistant nitrile gauntlets and FFP3 respirator. Keep upright; do not tilt or sniff.",
            "இரசாயன எதிர்ப்பு கையுறைகள் மற்றும் முகக்கவசம் அணியுங்கள். முகர்ந்து பார்க்கவோ சாய்க்கவோ கூடாது.",
            "रसायन-रोधी दस्ताने और मास्क पहनें। बोतल को सीधा रखें, कभी सूंघें नहीं।",
            "Corrosion-resistant HDPE drum with secondary spill-containment tray.",
            "அரிப்பு எதிர்ப்பு எச்.டி.பி.இ (HDPE) கொள்கலன்.",
            "संक्षारण प्रतिरोधी एचडीपीई ड्रम एवं सेकेंडरी कंटेनमेंट ट्रे।",
            "Authorized hazardous waste treatment, storage, and disposal facility (TSDF).",
            "அங்கீகரிக்கப்பட்ட அபாயகரமான இரசாயன கழிவு சுத்திகரிப்பு மையம் (TSDF).",
            "प्रमाणित खतरनाक अपशिष्ट उपचार एवं निपटान सुविधा (TSDF)।"
        ),
        (
            "aerosol",
            "MEDIUM",
            "Pressurized Aerosol / Spray Can",
            "அழுத்தப்பட்ட ஸ்ப்ரே கேன்கள் (Aerosol Can)",
            "दबावयुक्त एरोसोल / स्प्रे कैन (Aerosol)",
            "Pick up by main cylinder using puncture gloves. Store away from direct sunlight, friction, and heat.",
            "கையுறையுடன் உடற்பகுதியை பிடித்து எடுங்கள். வெப்பம் அல்லது தீப்பொறியிலிருந்து தூர வைக்கவும்.",
            "सुरक्षात्मक दस्ताने पहनकर उठाएं। सीधी धूप, गर्मी और चिंगारी से दूर रखें।",
            "Ventilated spark-proof metal cage or heavy perforated container.",
            "காற்றோட்டமான, தீப்பொறி படாத பாதுகாப்பு கூண்டு.",
            "हवादार और गैर-प्रज्वलनशील सुरक्षा कंटेनर।",
            "Controlled industrial depressurization and scrap metal recycling stream.",
            "அழுத்தம் நீக்கும் உலோக மறுசுழற்சி பிரிவு.",
            "नियंत्रित दबाव मुक्ति एवं धातु पुनर्चक्रण इकाई।"
        ),
        (
            "ewaste",
            "LOW",
            "Electronic Waste / Small Appliances",
            "மின்னணுக் கழிவு (E-Waste)",
            "ई-कचरा / छोटे उपकरण (E-Waste)",
            "Wear general duty work gloves. Bundle loose cables and handle without smashing internal boards.",
            "வேலை கையுறைகளை அணியுங்கள். பாகங்களை உடைக்காமல் முழுமையாகப் பிரித்து எடுங்கள்.",
            "हाथों में दस्ताने पहनें और सर्किट बोर्ड को तोड़े बिना सावधानी से उठाएं।",
            "Heavy-duty pallet bin or weather-proof crate.",
            "வலுவான பிளாஸ்டிக் அல்லது மரப் பெட்டி.",
            "मजबूत वेदर-प्रूफ क्रेट या स्टोरेज बिन।",
            "Authorized WEEE dismantling facility for copper, gold, and plastic recovery.",
            "அங்கீகரிக்கப்பட்ட மின்னணுக் கழிவு மறுசுழற்சி பிரிவு.",
            "अधिकृत ई-अपशिष्ट निराकरण एवं कीमती धातु पुनर्चक्रण केंद्र।"
        ),
        (
            "biomedical",
            "HIGH",
            "Biomedical / Soiled Sanitary Waste",
            "மருத்துவ / சுகாதாரக் கழிவு (Biomedical)",
            "जैव-चिकित्सा अपशिष्ट / सैनिटरी कचरा (Biomedical)",
            "Use elbow-length impermeable gloves and grabber tongs. Sanitize hands immediately after.",
            "நீண்ட கையுறைகள் மற்றும் இடுக்கியைப் பயன்படுத்துங்கள். உடனே கிருமிநாசினி தெளிக்கவும்.",
            "कोहनी तक के डिस्पोजेबल दस्ताने और चिमटे पहनें। तुरंत हाथों को सैनिटाइज करें।",
            "Double-bagged leakproof red or yellow biohazard bag with zip tie.",
            "இரட்டை உறை கொண்ட மஞ்சள்/சிவப்பு உயிரியல் அபாயப் பை.",
            "दोहरी परत वाला पीला या लाल बायोहाज़र्ड सीलबंद बैग।",
            "Common Bio-medical Waste Treatment Facility (CBWTF) high-heat incineration.",
            "அரசு அங்கீகாரம் பெற்ற மருத்துவக் கழிவு சுத்திகரிப்பு ஆலை (CBWTF).",
            "सामान्य जैव-चिकित्सा अपशिष्ट उपचार सुविधा (CBWTF)।"
        ),
        (
            "unknown",
            "MEDIUM",
            "Unidentified / Suspicious Substance",
            "அடையாளம் தெரியாத பொருள் (Unknown Hazard)",
            "अज्ञात / संदिग्ध वस्तु (Unknown)",
            "Do not touch, shake, or inhale. Immediately cordon off and alert facility safety supervisor.",
            "தொடவோ நுகரவோ குலுக்கவோ வேண்டாம். மேற்பார்வையாளர் ஆய்வுக்கு தனிமைப்படுத்தவும்.",
            "न छुएं, न हिलाएं और न सूंघें। तुरंत अलग कर सुरक्षा अधिकारी को सूचित करें।",
            "Transparent sealed quarantine box with hazard warning sticker.",
            "வெளிப்படையான காற்றுப் புகாத தனிமைப்படுத்தல் கொள்கலன்.",
            "पारदर्शी सीलबंद क्वारंटाइन कंटेनर।",
            "Quarantine isolation until on-site inspection by HazMat response team.",
            "பாதுகாப்பு அதிகாரி ஆய்வு செய்யும் வரை தனிமைப்படுத்தி வைக்கவும்.",
            "विशेषज्ञ जांच एवं सुरक्षा समीक्षा तक क्वारंटाइन में सुरक्षित रखें।"
        ),
        (
            "safe",
            "LOW",
            "Safe Dry Recyclable Waste",
            "பாதுகாப்பான உலர் மறுசுழற்சிக் கழிவு (Safe Dry)",
            "सुरक्षित सूखा पुनर्चक्रण योग्य कचरा (Safe Dry)",
            "Standard dry sorting work gloves. Sort into paper, clean plastics, and cardboard.",
            "சாதாரண வேலை கையுறைகளைப் பயன்படுத்தி பேப்பர், அட்டை, பிளாஸ்டிக்கைப் பிரிக்கலாம்.",
            "सामान्य दस्ताने पहनकर सूखे कागज, गत्ते और प्लास्टिक को अलग करें।",
            "Standard green/blue dry waste sorting hopper.",
            "வழக்கமான உலர் கழிவுத் தொட்டி (நீலம்/பச்சை).",
            "सामान्य नीला/हरा सूखा कचரா बिन।",
            "Municipal Material Recovery Facility (MRF) baling and circular economy processing.",
            "நகராட்சி உலர் கழிவு மீட்பு மையம் (MRF).",
            "सामुदायिक अपशिष्ट पुनर्चक्रण सुविधा (MRF)।"
        ),
    ]

    for hc in hazard_classes:
        cur.execute("""
            INSERT INTO hazard_classes (
                code, severity, name_en, name_ta, name_hi,
                pickup_en, pickup_ta, pickup_hi,
                container_en, container_ta, container_hi,
                disposal_en, disposal_ta, disposal_hi
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET
                severity=excluded.severity,
                name_en=excluded.name_en,
                name_ta=excluded.name_ta,
                name_hi=excluded.name_hi,
                pickup_en=excluded.pickup_en,
                pickup_ta=excluded.pickup_ta,
                pickup_hi=excluded.pickup_hi,
                container_en=excluded.container_en,
                container_ta=excluded.container_ta,
                container_hi=excluded.container_hi,
                disposal_en=excluded.disposal_en,
                disposal_ta=excluded.disposal_ta,
                disposal_hi=excluded.disposal_hi
        """, hc)
    print(f"✓ Seeded {len(hazard_classes)} hazard classes.")

    # 3. Seed Realistic Demonstration Bags & Lifecycle Chain of Custody
    cur.execute("SELECT id, employee_id FROM users WHERE employee_id IN ('EMP101', 'EMP102')")
    collectors = {r[1]: r[0] for r in cur.fetchall()}
    emp101_id = collectors.get('EMP101', 2)
    emp102_id = collectors.get('EMP102', 3)

    sample_bags = [
        ("SS1001", "tok_ss1001_" + str(uuid.uuid4())[:8], "Zone-A", "Dry domestic waste collected from Anna Nagar Market block", emp101_id, "registered", "UNVERIFIED", 0, 0),
        ("SS1002", "tok_ss1002_" + str(uuid.uuid4())[:8], "Zone-A", "Commercial shop dry refuse from 4th Avenue", emp101_id, "analysed", "HIGH", 1, 1),
        ("SS1003", "tok_ss1003_" + str(uuid.uuid4())[:8], "Zone-B", "Residential dry sack from Shastri Nagar apartments", emp102_id, "received", "MEDIUM", 1, 0),
        ("SS1004", "tok_ss1004_" + str(uuid.uuid4())[:8], "Zone-B", "School office paper and dry packaging waste", emp102_id, "segregated", "LOW", 1, 0),
        ("SS1005", "tok_ss1005_" + str(uuid.uuid4())[:8], "Zone-A", "Mixed dry bag with discarded clinic packaging", emp101_id, "disposed", "HIGH", 1, 0)
    ]

    for b in sample_bags:
        cur.execute("""
            INSERT INTO bags (bag_code, qr_token, zone, source_note, collector_id, status, risk_level, ppe_confirmed, needs_review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(bag_code) DO NOTHING
        """, b)
        try:
            from services.qr_service import generate_qr_code
            generate_qr_code(b[0], b[1])
        except Exception as e:
            print(f"[WARN] Failed to generate QR during seed: {e}")
    print(f"✓ Seeded sample bags and generated QR codes.")

    # 4. Seed Detections for Analysed & Received Bags
    cur.execute("SELECT id, bag_code FROM bags")
    bag_map = {r[1]: r[0] for r in cur.fetchall()}

    if "SS1002" in bag_map:
        ss1002_id = bag_map["SS1002"]
        cur.execute("DELETE FROM detections WHERE bag_id = ?", (ss1002_id,))
        cur.execute("""
            INSERT INTO detections (bag_id, item_name, hazard_class, severity, confidence, needs_review, review_decision, analysis_ms, segregated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ss1002_id, "Corroded Alkaline AA Battery Pack", "battery", "HIGH", 0.94, 1, "pending_review", 340, 0))
        cur.execute("""
            INSERT INTO detections (bag_id, item_name, hazard_class, severity, confidence, needs_review, review_decision, analysis_ms, segregated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ss1002_id, "Discarded Syringe with Plunger", "sharps", "HIGH", 0.89, 1, "pending_review", 310, 0))

    if "SS1003" in bag_map:
        ss1003_id = bag_map["SS1003"]
        cur.execute("DELETE FROM detections WHERE bag_id = ?", (ss1003_id,))
        cur.execute("""
            INSERT INTO detections (bag_id, item_name, hazard_class, severity, confidence, needs_review, review_decision, analysis_ms, segregated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ss1003_id, "Shattered Mirror Shards", "glass", "MEDIUM", 0.96, 0, "approved", 280, 0))

    if "SS1004" in bag_map:
        ss1004_id = bag_map["SS1004"]
        cur.execute("DELETE FROM detections WHERE bag_id = ?", (ss1004_id,))
        cur.execute("""
            INSERT INTO detections (bag_id, item_name, hazard_class, severity, confidence, needs_review, review_decision, analysis_ms, segregated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ss1004_id, "Clean Office Paper & Cardboard", "safe", "LOW", 0.98, 0, "approved", 195, 1))

    # 5. Seed Status Events
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for bcode, bid in bag_map.items():
        cur.execute("""
            INSERT INTO status_events (bag_id, status, user_id, ts, note)
            VALUES (?, ?, ?, ?, ?)
        """, (bid, "registered", emp101_id, now_str, f"Bag {bcode} registered at collection point"))

    # 6. Seed Sample Incidents
    cur.execute("DELETE FROM incidents")
    cur.execute("""
        INSERT INTO incidents (bag_id, reporter_id, type, description, zone, ts)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (bag_map.get("SS1002"), emp101_id, "near_miss", "Uncapped needle tip observed protruding through outer bag liner. Avoided puncture using tongs.", "Zone-A", now_str))

    # 7. Seed Sample Evaluation Run
    cur.execute("DELETE FROM eval_runs")
    cur.execute("""
        INSERT INTO eval_runs (n_images, accuracy, precision_, recall, avg_ms)
        VALUES (?, ?, ?, ?, ?)
    """, (50, 0.942, 0.925, 0.950, 265.4))

    # 8. Seed Audit Log
    cur.execute("DELETE FROM audit_log")
    cur.execute("""
        INSERT INTO audit_log (user_id, action, target, details, ts)
        VALUES (?, ?, ?, ?, ?)
    """, (1, "SYSTEM_SEED", "database", "Idempotent seed executed with users, hazard classes, and test bags", now_str))

    conn.commit()
    conn.close()
    print("✓ SafeSack 360 database seed completed successfully.")


if __name__ == "__main__":
    seed_database()
