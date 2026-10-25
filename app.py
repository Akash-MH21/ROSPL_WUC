from flask import Flask, render_template, request
import ipaddress
import socket
import time
from urllib.parse import urlparse

import requests

app = Flask(__name__)


def is_public_host(hostname):
    """Basic guard against checking localhost/private network addresses."""
    if not hostname:
        return False

    if hostname.lower() == "localhost" or hostname.lower().endswith(".localhost"):
        return False

    try:
        addresses = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    for address in addresses:
        try:
            ip = ipaddress.ip_address(address[4][0])
        except ValueError:
            return False
        if not ip.is_global:
            return False

    return True


def check_website(url):
    result = {
        "url": url,
        "status": "Offline",
        "status_code": "N/A",
        "response_time": "N/A",
        "message": "",
    }

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        result.update(status="Invalid", message="Enter a valid HTTP or HTTPS URL.")
        return result

    if not is_public_host(parsed.hostname):
        result.update(
            status="Blocked",
            message="Hostname could not be resolved or points to a local/private network.",
        )
        return result

    try:
        start = time.perf_counter()
        response = requests.get(
            url,
            timeout=8,
            allow_redirects=False,
            headers={"User-Agent": "ROSPL-WUC/1.0"},
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        result["status_code"] = response.status_code
        result["response_time"] = round(elapsed_ms, 2)

        if 200 <= response.status_code < 400:
            result.update(status="Online", message="Website responded successfully.")
        else:
            result.update(status="Offline", message="Website returned an HTTP error.")
    except requests.RequestException:
        result.update(status="Offline", message="Website could not be reached.")

    return result


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url or len(url) > 2048:
            result = {
                "url": url,
                "status": "Invalid",
                "status_code": "N/A",
                "response_time": "N/A",
                "message": "Please enter a URL (maximum 2048 characters).",
            }
        else:
            if "://" not in url:
                url = "https://" + url
            result = check_website(url)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    # Debug is disabled by default for safer local use.
    app.run(host="127.0.0.1", port=5000, debug=False)
