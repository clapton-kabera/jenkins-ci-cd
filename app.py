"""A small Flask web service for the Jenkins CI/CD lab."""
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# Set at deploy time (e.g. docker run -e APP_VERSION=$BUILD_NUMBER) so you can
# see in the browser exactly which build is running. Defaults to "dev".
APP_VERSION = os.environ.get("APP_VERSION", "dev")


def add_numbers(a, b):
    """Pure function, kept separate from the route so it's easy to unit test."""
    return a + b


@app.route("/")
def index():
    return (
        "<!doctype html>"
        "<title>Flask CI/CD Lab</title>"
        "<h1>Hello from the Jenkins pipeline!</h1>"
        f"<p>Version: <strong>{APP_VERSION}</strong></p>"
    )


@app.route("/health")
def health():
    """Used by smoke tests and monitoring to check the app is up."""
    return jsonify(status="ok", version=APP_VERSION)


@app.route("/api/add")
def add():
    """Example: /api/add?a=2&b=3 returns {"result": 5.0}."""
    try:
        a = float(request.args["a"])
        b = float(request.args["b"])
    except KeyError:
        return jsonify(error="Both 'a' and 'b' query parameters are required"), 400
    except ValueError:
        return jsonify(error="'a' and 'b' must be numbers"), 400
    return jsonify(result=add_numbers(a, b))


if __name__ == "__main__":
    # Local development only. In the container, gunicorn runs the app instead.
    app.run(host="0.0.0.0", port=5000, debug=True)
