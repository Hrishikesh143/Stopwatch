from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# -----------------------------
# Prometheus Metrics
# -----------------------------

REQUEST_COUNT = Counter(
    "stopwatch_requests_total",
    "Total HTTP requests"
)

COUNTDOWN_STARTED = Counter(
    "stopwatch_countdown_started_total",
    "Total countdowns started"
)

COUNTDOWN_COMPLETED = Counter(
    "stopwatch_countdown_completed_total",
    "Total countdowns completed"
)

REQUEST_LATENCY = Histogram(
    "stopwatch_request_duration_seconds",
    "Request latency in seconds"
)

# -----------------------------
# Middleware
# -----------------------------

@app.before_request
def before_request():
    request.start_time = time.time()
    REQUEST_COUNT.inc()


@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.observe(latency)
    return response


# -----------------------------
# Authentication Pages
# -----------------------------

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("index.html")


@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


# -----------------------------
# Placeholder APIs
# -----------------------------

@app.route("/register", methods=["POST"])
def register():
    """
    This will later insert user details into PostgreSQL.
    """
    data = request.get_json()

    return jsonify({
        "status": "success",
        "message": "Registration endpoint is ready.",
        "data": data
    })


@app.route("/login", methods=["POST"])
def login_user():
    """
    This will later validate user credentials from PostgreSQL.
    """
    data = request.get_json()

    return jsonify({
        "status": "success",
        "message": "Login endpoint is ready.",
        "data": data
    })


# -----------------------------
# Stopwatch APIs
# -----------------------------

@app.route("/start", methods=["POST"])
def start():

    COUNTDOWN_STARTED.inc()

    data = request.get_json()
    seconds = int(data.get("seconds", 0))

    return jsonify({
        "status": "started",
        "seconds": seconds
    })


@app.route("/complete", methods=["POST"])
def complete():

    COUNTDOWN_COMPLETED.inc()

    return jsonify({
        "status": "completed"
    })


# -----------------------------
# Prometheus Metrics
# -----------------------------

@app.route("/metrics")
def metrics():

    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
