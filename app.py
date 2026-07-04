from flask import Flask, render_template, request, jsonify, Response
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
# Routes
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


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


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
