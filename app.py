import os
from flask import Flask, redirect, url_for, send_file, request, jsonify
from flask_login import LoginManager, current_user
from dotenv import load_dotenv

from db import close_db, init_db, query_db
from blueprints.auth import auth_bp, load_user_by_id
from blueprints.collector import collector_bp
from blueprints.disposer import disposer_bp
from blueprints.admin import admin_bp
from services.tts_service import generate_audio_instruction

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'safesack360-hazard-detection-secret-2026')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max image upload

# Ensure static directories exist
for folder in ['audio', 'qr', 'uploads', 'model', 'css', 'js', 'i18n']:
    os.makedirs(os.path.join(app.static_folder, folder), exist_ok=True)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return load_user_by_id(int(user_id))

# Teardown database connection
app.teardown_appcontext(close_db)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(collector_bp)
app.register_blueprint(disposer_bp)
app.register_blueprint(admin_bp)


@app.template_filter('dt')
def format_datetime(val):
    """Safely format strings, datetimes, or None for UI display."""
    if not val:
        return '-'
    if hasattr(val, 'strftime'):
        return val.strftime('%Y-%m-%d %H:%M')
    return str(val)[:16]



@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'collector':
            return redirect(url_for('collector.dashboard'))
        elif current_user.role == 'disposer':
            return redirect(url_for('disposer.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))


@app.route('/api/hazard-audio/<hazard_code>')
def hazard_audio(hazard_code):
    lang = request.args.get('lang', 'en')
    if lang not in ('en', 'ta', 'hi'):
        lang = 'en'

    # Fetch hazard instructions from database
    hazard = query_db("SELECT * FROM hazard_classes WHERE code = ?", (hazard_code,), one=True)
    if not hazard:
        return jsonify({'error': 'Hazard class not found'}), 404

    # Select text for requested language
    field_name = f"pickup_{lang}"
    guidance_text = hazard[field_name] if field_name in hazard.keys() else hazard['pickup_en']

    audio_path = generate_audio_instruction(guidance_text, hazard_code, lang)
    if audio_path:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), audio_path.lstrip('/'))
        if os.path.exists(full_path):
            return send_file(full_path, mimetype='audio/mpeg')

    return jsonify({'message': 'Audio synthesis unavailable, use browser text-to-speech fallback'}), 204


def ensure_database_ready():
    """Ensure database schema is created and seeded with default data."""
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'safesack360.db')
    try:
        import sqlite3
        from seed import seed_database
        if not os.path.exists(db_file):
            print("Database not found. Initializing and running seed...")
            seed_database()
        else:
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users")
            count = cur.fetchone()[0]
            conn.close()
            if count == 0:
                print("Database exists but has 0 users. Seeding...")
                seed_database()
    except Exception as e:
        print(f"[WARN] Database initialization check: {e}")
        try:
            from seed import seed_database
            seed_database()
        except Exception as seed_err:
            print(f"[ERROR] Seed execution error: {seed_err}")

    try:
        from services.demo_assets import generate_demo_images
        generate_demo_images()
    except Exception as demo_err:
        print(f"[WARN] Failed generating demo assets: {demo_err}")

    try:
        from services.eval_assets import generate_eval_assets
        generate_eval_assets()
    except Exception as eval_err:
        print(f"[WARN] Failed generating eval assets: {eval_err}")

    # Ensure demo seed is run if database is sparse (< 10 bags)
    try:
        from seed_demo import seed_demo_database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM bags")
        bag_count = c.fetchone()[0]
        conn.close()
        if bag_count < 10:
            print("[SEED] Running full 25-bag demo simulation seed...")
            seed_demo_database()
    except Exception as seed_demo_err:
        print(f"[WARN] Demo seed check: {seed_demo_err}")

    # Pre-generate fixed multilingual voice alert MP3s in background
    try:
        import threading
        from scripts.generate_audio import generate_all_audio
        audio_thread = threading.Thread(target=generate_all_audio, daemon=True)
        audio_thread.start()
    except Exception as audio_err:
        print(f"[WARN] Failed background audio generation: {audio_err}")

    # Run startup data retention cleanup check
    try:
        from services.retention_service import startup_retention_check
        startup_retention_check()
    except Exception as ret_err:
        print(f"[WARN] Startup retention check: {ret_err}")


# Ensure DB ready on load
ensure_database_ready()


@app.route('/api/audio-alert/<alert_key>')
def audio_alert(alert_key):
    lang = request.args.get('lang', 'en')
    if lang not in ('en', 'ta', 'hi'):
        lang = 'en'

    target_path = os.path.join(app.static_folder, 'audio', lang, f"{alert_key}.mp3")
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return send_file(target_path, mimetype='audio/mpeg')

    # If missing, attempt fast on-demand synthesis and cache
    try:
        from scripts.generate_audio import MESSAGES
        if alert_key in MESSAGES and lang in MESSAGES[alert_key]:
            from gtts import gTTS
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            tts = gTTS(text=MESSAGES[alert_key][lang], lang=lang, slow=False)
            tts.save(target_path)
            return send_file(target_path, mimetype='audio/mpeg')
    except Exception as e:
        print(f"[WARN] On-demand gTTS failed for {alert_key}_{lang}: {e}")

    return jsonify({'error': 'Audio alert unavailable', 'key': alert_key}), 404


if __name__ == '__main__':
    print("=" * 60)
    print(" SafeSack 360 - Hazard-Detection & Chain-of-Custody System")
    print(" Running on: http://0.0.0.0:5000")
    print(" Demo Logins (Password: demo123):")
    print("   - Admin:     EMP001")
    print("   - Collector: EMP101, EMP102")
    print("   - Disposer:  EMP201")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)

