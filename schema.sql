-- SafeSack 360 Database Schema (SQLite)

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    employee_id TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('collector', 'disposer', 'admin')),
    phone TEXT,
    zone TEXT,
    password_hash TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE IF NOT EXISTS login_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    employee_id TEXT NOT NULL,
    success INTEGER NOT NULL,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS hazard_classes (
    code TEXT PRIMARY KEY,
    severity TEXT NOT NULL CHECK(severity IN ('HIGH', 'MEDIUM', 'LOW')),
    name_en TEXT NOT NULL,
    name_ta TEXT NOT NULL,
    name_hi TEXT NOT NULL,
    pickup_en TEXT NOT NULL,
    pickup_ta TEXT NOT NULL,
    pickup_hi TEXT NOT NULL,
    container_en TEXT NOT NULL,
    container_ta TEXT NOT NULL,
    container_hi TEXT NOT NULL,
    disposal_en TEXT NOT NULL,
    disposal_ta TEXT NOT NULL,
    disposal_hi TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bag_code TEXT UNIQUE NOT NULL,
    qr_token TEXT UNIQUE NOT NULL,
    qr_status TEXT NOT NULL DEFAULT 'active' CHECK(qr_status IN ('active', 'disabled', 'deleted')),
    zone TEXT NOT NULL,
    source_note TEXT,
    collector_id INTEGER,
    status TEXT NOT NULL DEFAULT 'registered' CHECK(status IN ('registered', 'opened', 'analysed', 'labelled', 'received', 'segregated', 'disposed', 'unverified')),
    risk_level TEXT NOT NULL DEFAULT 'UNVERIFIED' CHECK(risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'UNVERIFIED')),
    ppe_confirmed INTEGER NOT NULL DEFAULT 0,
    needs_review INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    labelled_at TIMESTAMP,
    received_at TIMESTAMP,
    disposed_at TIMESTAMP,
    FOREIGN KEY(collector_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS bag_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bag_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(bag_id) REFERENCES bags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bag_id INTEGER NOT NULL,
    image_id INTEGER,
    item_name TEXT NOT NULL,
    hazard_class TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('HIGH', 'MEDIUM', 'LOW')),
    confidence REAL,
    needs_review INTEGER NOT NULL DEFAULT 0,
    review_decision TEXT,
    reviewed_by INTEGER,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analysis_ms INTEGER,
    segregated INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(bag_id) REFERENCES bags(id) ON DELETE CASCADE,
    FOREIGN KEY(image_id) REFERENCES bag_images(id) ON DELETE SET NULL,
    FOREIGN KEY(hazard_class) REFERENCES hazard_classes(code),
    FOREIGN KEY(reviewed_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS status_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bag_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    user_id INTEGER,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note TEXT,
    FOREIGN KEY(bag_id) REFERENCES bags(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bag_id INTEGER,
    reporter_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('near_miss', 'injury', 'suspicious_bag', 'unlabeled_bag')),
    description TEXT NOT NULL,
    zone TEXT NOT NULL,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(bag_id) REFERENCES bags(id) ON DELETE SET NULL,
    FOREIGN KEY(reporter_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    detection_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    verdict TEXT NOT NULL CHECK(verdict IN ('correct', 'false_positive', 'missed_hazard')),
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(detection_id) REFERENCES detections(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    details TEXT,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS eval_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    n_images INTEGER NOT NULL,
    accuracy REAL NOT NULL,
    precision_ REAL NOT NULL,
    recall REAL NOT NULL,
    avg_ms REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_bags_bag_code ON bags(bag_code);
CREATE INDEX IF NOT EXISTS idx_bags_qr_token ON bags(qr_token);
CREATE INDEX IF NOT EXISTS idx_bags_status ON bags(status);
CREATE INDEX IF NOT EXISTS idx_detections_bag ON detections(bag_id);
CREATE INDEX IF NOT EXISTS idx_status_events_bag ON status_events(bag_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
