import os
import random
import uuid
from datetime import datetime, timedelta
import sqlite3

from services.qr_service import generate_qr_code

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'safesack360.db')


def seed_demo_database():
    """
    Seeds ~25 municipal waste bags across the last 20 days with realistic hazard
    detections, status transitions, safety incidents, worker feedback, login histories,
    and audit logs.

    All generated records are explicitly tagged as [SIMULATED].
    Includes 3 bags awaiting receipt (>10 mins elapsed) for live coordination-gap demonstration.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    # 1. Fetch user IDs
    cur.execute("SELECT id, role, zone FROM users")
    users = cur.fetchall()
    user_map = {row[1]: row[0] for row in users}  # role -> id
    admin_id = user_map.get('admin', 1)
    collector_id = user_map.get('collector', 2)
    disposer_id = user_map.get('disposer', 3)

    now = datetime.now()

    # 2. Define the 25 bags specification
    # Bags 1 to 22 span across 1 to 19 days ago
    # Bags 23, 24, 25 are today's live coordination-gap bags awaiting receipt
    bag_configs = [
        # (offset_days, zone, status, risk, ppe, needs_review, item_tuples)
        (19, 'Zone-A', 'disposed', 'HIGH', 1, 0, [('battery', 'AA Alkaline Battery Cell', 'HIGH', 0.94), ('safe', 'Dry Cardboard Carton', 'LOW', 0.98)]),
        (18, 'Zone-B', 'disposed', 'MEDIUM', 1, 0, [('glass', 'Fractured Beer Bottle', 'MEDIUM', 0.88)]),
        (17, 'Zone-A', 'disposed', 'LOW', 1, 0, [('safe', 'Crushed PET Water Bottles', 'LOW', 0.96)]),
        (16, 'Zone-C', 'disposed', 'HIGH', 1, 0, [('sharps', 'Used Insulin Syringe', 'HIGH', 0.92)]),
        (15, 'Zone-B', 'disposed', 'HIGH', 1, 0, [('chemical', 'Unmarked Solvent Bottle', 'HIGH', 0.89)]),
        (14, 'Zone-A', 'disposed', 'LOW', 1, 0, [('safe', 'Office Paper Reams', 'LOW', 0.99)]),
        (13, 'Zone-D', 'disposed', 'MEDIUM', 1, 0, [('aerosol', 'Discarded Spray Paint Can', 'MEDIUM', 0.85)]),
        (12, 'Zone-C', 'disposed', 'HIGH', 1, 0, [('lamp_cfl', 'Broken CFL Mercury Bulb', 'HIGH', 0.91), ('glass', 'Glass Shards', 'MEDIUM', 0.87)]),
        (11, 'Zone-B', 'segregated', 'HIGH', 1, 0, [('battery', 'Lithium Pouch Battery', 'HIGH', 0.95)]),
        (10, 'Zone-A', 'segregated', 'MEDIUM', 1, 0, [('glass', 'Shattered Mirror Shards', 'MEDIUM', 0.86)]),
        (9, 'Zone-C', 'segregated', 'LOW', 1, 0, [('ewaste', 'Old Telecom Wiring & Charger', 'LOW', 0.84)]),
        (8, 'Zone-B', 'received', 'HIGH', 1, 0, [('chemical', 'Acid Drain Cleaner Jug', 'HIGH', 0.93)]),
        (7, 'Zone-D', 'received', 'HIGH', 1, 0, [('sharps', 'Surgical Needle & Syringe', 'HIGH', 0.96)]),
        (6, 'Zone-A', 'received', 'LOW', 1, 0, [('safe', 'Polyethylene Packing Foam', 'LOW', 0.92)]),
        (5, 'Zone-C', 'analysed', 'HIGH', 1, 0, [('battery', 'Corroded 9V Battery Cell', 'HIGH', 0.91)]),
        (4, 'Zone-B', 'analysed', 'MEDIUM', 1, 0, [('aerosol', 'Deodorant Aerosol Canister', 'MEDIUM', 0.83)]),
        (3, 'Zone-A', 'opened', 'LOW', 1, 0, [('safe', 'Dry Shredded Packaging Paper', 'LOW', 0.95)]),
        (2, 'Zone-D', 'opened', 'HIGH', 1, 1, [('battery', 'Unrecognised Battery Pack', 'HIGH', 0.64)]),
        (2, 'Zone-A', 'registered', 'UNVERIFIED', 0, 0, []),
        (1, 'Zone-B', 'registered', 'UNVERIFIED', 0, 0, []),
        (1, 'Zone-C', 'unverified', 'UNVERIFIED', 1, 1, [('unknown', 'Unknown Toxic Bag - Quarantined', 'HIGH', 0.55)]),
        (1, 'Zone-A', 'unverified', 'UNVERIFIED', 1, 0, []),

        # === 3 Bags specifically awaiting receipt for Coordination Gap Demo ===
        # SS1023: Labelled 35 minutes ago in Zone-A (>10m default threshold)
        (0.024, 'Zone-A', 'labelled', 'HIGH', 1, 0, [('battery', 'Rechargeable Li-Ion Cell', 'HIGH', 0.93)]),
        # SS1024: Labelled 75 minutes ago in Zone-B
        (0.052, 'Zone-B', 'labelled', 'HIGH', 1, 0, [('sharps', 'Disposable Lancet & Needle', 'HIGH', 0.97)]),
        # SS1025: Labelled 160 minutes ago in Zone-C
        (0.111, 'Zone-C', 'labelled', 'MEDIUM', 1, 0, [('glass', 'Cracked Beverage Bottle', 'MEDIUM', 0.86)])
    ]

    print(f"[SEED] Starting simulated demo seed ({len(bag_configs)} bags across 20 days)...")

    # Clear existing bags and child records to maintain clean demo state if needed
    cur.execute("DELETE FROM bags WHERE source_note LIKE '%[SIMULATED]%'")
    cur.execute("DELETE FROM login_log WHERE employee_id IN ('EMP001', 'EMP101', 'EMP102', 'EMP201') AND ts < datetime('now', '-1 hour')")
    cur.execute("DELETE FROM incidents WHERE description LIKE '%[SIMULATED]%'")
    cur.execute("DELETE FROM audit_log WHERE details LIKE '%[SIMULATED]%'")

    created_bag_ids = []
    created_detection_ids = []

    for idx, (days_ago, zone, status, risk, ppe, needs_rev, items) in enumerate(bag_configs, start=1):
        bag_code = f"SS{1000 + idx}"
        qr_token = f"tok_{bag_code.lower()}_{uuid.uuid4().hex[:8]}"

        created_dt = now - timedelta(days=days_ago)
        created_str = created_dt.strftime("%Y-%m-%d %H:%M:%S")

        labelled_str = None
        received_str = None
        disposed_str = None

        if status in ('labelled', 'received', 'segregated', 'disposed'):
            labelled_dt = created_dt + timedelta(minutes=random.randint(5, 20))
            labelled_str = labelled_dt.strftime("%Y-%m-%d %H:%M:%S")

        if status in ('received', 'segregated', 'disposed'):
            received_dt = created_dt + timedelta(minutes=random.randint(25, 60))
            received_str = received_dt.strftime("%Y-%m-%d %H:%M:%S")

        if status == 'disposed':
            disposed_dt = created_dt + timedelta(minutes=random.randint(70, 140))
            disposed_str = disposed_dt.strftime("%Y-%m-%d %H:%M:%S")

        source_note = f"[SIMULATED] Municipal dry waste collection route #{100 + (idx % 8)} ({zone})"

        cur.execute(
            """INSERT INTO bags (bag_code, qr_token, qr_status, zone, source_note, collector_id, status, risk_level, ppe_confirmed, needs_review, created_at, labelled_at, received_at, disposed_at)
               VALUES (?, ?, 'active', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (bag_code, qr_token, zone, source_note, collector_id, status, risk, ppe, needs_rev, created_str, labelled_str, received_str, disposed_str)
        )
        bag_id = cur.lastrowid
        created_bag_ids.append((bag_id, bag_code, status))

        # Generate QR code png
        try:
            generate_qr_code(bag_code, qr_token)
        except Exception:
            pass

        # Insert Status Events
        cur.execute(
            """INSERT INTO status_events (bag_id, status, user_id, ts, note)
               VALUES (?, 'registered', ?, ?, '[SIMULATED] Sack intake registered at collection point.')""",
            (bag_id, collector_id, created_str)
        )
        if ppe:
            cur.execute(
                """INSERT INTO status_events (bag_id, status, user_id, ts, note)
                   VALUES (?, 'ppe_confirmed', ?, ?, '[SIMULATED] No-Touch PPE safety gate confirmed.')""",
                (bag_id, collector_id, created_str)
            )
        if labelled_str:
            cur.execute(
                """INSERT INTO status_events (bag_id, status, user_id, ts, note)
                   VALUES (?, 'labelled', ?, ?, '[SIMULATED] AI classification completed and QR label issued.')""",
                (bag_id, collector_id, labelled_str)
            )
        if received_str:
            cur.execute(
                """INSERT INTO status_events (bag_id, status, user_id, ts, note)
                   VALUES (?, 'received', ?, ?, '[SIMULATED] Sack checked in at facility sorting dock.')""",
                (bag_id, disposer_id, received_str)
            )
        if status in ('segregated', 'disposed'):
            seg_str = (datetime.strptime(received_str, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
            cur.execute(
                """INSERT INTO status_events (bag_id, status, user_id, ts, note)
                   VALUES (?, 'segregated', ?, ?, '[SIMULATED] All hazards isolated into color-coded containment tubs.')""",
                (bag_id, disposer_id, seg_str)
            )
        if disposed_str:
            cur.execute(
                """INSERT INTO status_events (bag_id, status, user_id, ts, note)
                   VALUES (?, 'disposed', ?, ?, '[SIMULATED] Final certified disposal completed. QR code retired.')""",
                (bag_id, disposer_id, disposed_str)
            )

        # Insert Detections for this bag
        for hazard_code, item_name, severity, confidence in items:
            is_seg = 1 if status in ('segregated', 'disposed') else 0
            det_dt = created_dt + timedelta(minutes=3)
            det_str = det_dt.strftime("%Y-%m-%d %H:%M:%S")
            det_needs_rev = 1 if confidence < 0.70 else 0
            analysis_ms = random.randint(115, 230)

            cur.execute(
                """INSERT INTO detections (bag_id, item_name, hazard_class, severity, confidence, needs_review, detected_at, analysis_ms, segregated)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (bag_id, f"[SIMULATED] {item_name}", hazard_code, severity, confidence, det_needs_rev, det_str, analysis_ms, is_seg)
            )
            created_detection_ids.append(cur.lastrowid)

    # 3. Insert Realistic Field Safety Incidents
    simulated_incidents = [
        ('near_miss', 'Zone-A', 14, '[SIMULATED] Puncture hazard near-miss: Protruding syringe tip stopped by reinforced puncture-resistant gauntlets. Worker used mechanical tongs to isolate.'),
        ('injury', 'Zone-B', 8, '[SIMULATED] Minor cut to outer nitrile glove layer caused by broken fluorescent tube fragments. Skin barrier intact; worker replenished PPE immediately.'),
        ('suspicious_bag', 'Zone-C', 3, '[SIMULATED] Acrid chemical solvent fumes detected emanating from untagged plastic canister. Bag placed in chemical quarantine tub under Unknown Protocol.'),
        ('unlabeled_bag', 'Zone-D', 1, '[SIMULATED] Unlabeled waste sack discovered at receiving dock perimeter with biological hazard marking. Quarantined for supervisor visual inspection.')
    ]
    for inc_type, zone, days_ago, desc in simulated_incidents:
        inc_dt = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            """INSERT INTO incidents (reporter_id, type, description, zone, ts)
               VALUES (?, ?, ?, ?, ?)""",
            (collector_id, inc_type, desc, zone, inc_dt)
        )

    # 4. Insert Worker Accuracy Feedback (Correct, False Positive, Missed Hazard)
    if created_detection_ids:
        for idx, det_id in enumerate(created_detection_ids[:15]):
            if idx in (0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 13, 14):
                verdict = 'correct'
            elif idx in (4, 9):
                verdict = 'false_positive'
            else:
                verdict = 'missed_hazard'
            fb_time = (now - timedelta(days=max(1, 18 - idx))).strftime("%Y-%m-%d %H:%M:%S")
            cur.execute(
                """INSERT INTO feedback (detection_id, user_id, verdict, ts)
                   VALUES (?, ?, ?, ?)""",
                (det_id, disposer_id, verdict, fb_time)
            )

    # 5. Insert Historical Login Logs across 20 days
    login_users = [
        (admin_id, 'EMP001'),
        (collector_id, 'EMP101'),
        (collector_id, 'EMP102'),
        (disposer_id, 'EMP201')
    ]
    for d in range(19, 0, -1):
        day_date = now - timedelta(days=d)
        for u_id, emp_code in login_users:
            # 90% success, 10% simulated typo/failed attempt
            success = 1 if random.random() > 0.10 else 0
            login_time = (day_date + timedelta(hours=random.randint(6, 18), minutes=random.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S")
            cur.execute(
                """INSERT INTO login_log (user_id, employee_id, success, ts)
                   VALUES (?, ?, ?, ?)""",
                (u_id if success else None, emp_code, success, login_time)
            )

    # 6. Insert System Audit Trail Records
    audit_templates = [
        (admin_id, 'USER_CREATED', 'user:EMP102', '[SIMULATED] Provisioned collector credentials for Zone-B facility.'),
        (collector_id, 'BAG_REGISTERED', 'bag:SS1008', '[SIMULATED] Intake verification and custody tag generation.'),
        (collector_id, 'NO_TOUCH_GATE_PASSED', 'bag:SS1012', '[SIMULATED] All 5 PPE checklist safety criteria verified.'),
        (disposer_id, 'BAG_RECEIVED', 'bag:SS1005', '[SIMULATED] Physical QR scan accepted at facility dock.'),
        (disposer_id, 'QR_DISABLED', 'bag:SS1002', '[SIMULATED] QR tag disabled post certified material segregation.'),
        (admin_id, 'SETTING_UPDATED', 'coordination_gap_minutes', '[SIMULATED] Updated operational transit delay threshold to 10 minutes.')
    ]
    for idx, (u_id, action, target, details) in enumerate(audit_templates):
        a_time = (now - timedelta(days=max(1, 16 - (idx * 2)))).strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            """INSERT INTO audit_log (user_id, action, target, details, ts)
               VALUES (?, ?, ?, ?, ?)""",
            (u_id, action, target, details, a_time)
        )

    # 7. Add at least one baseline Eval Run
    cur.execute("SELECT COUNT(*) FROM eval_runs")
    if cur.fetchone()[0] == 0:
        cur.execute(
            """INSERT INTO eval_runs (n_images, accuracy, precision_, recall, avg_ms, ts)
               VALUES (14, 0.928, 0.915, 0.932, 138.4, ?)""",
            ((now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),)
        )

    conn.commit()
    conn.close()

    print(f"✓ Successfully seeded {len(bag_configs)} bags (including 3 coordination-gap bags awaiting receipt).")
    print("✓ Realistic detections, incidents, feedback, logins, and audit logs populated.")


if __name__ == '__main__':
    seed_demo_database()
