from flask import Flask, render_template, request, send_file
import os
from datetime import datetime
import random
import io

app = Flask(__name__)

scan_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    file = request.files["file"]
    filename = file.filename
    size_kb = round(len(file.read()) / 1024, 2)

    # Dummy threat detection
    threats_found = random.choice([0, 0, 0, 1])  # 25% chance to find threat
    clean_files = 1 if threats_found == 0 else 0
    total_files = 1

    status = "No Threats Found" if threats_found == 0 else "Threat Detected!"
    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store in history
    scan_history.append({
        "file": filename,
        "size": f"{size_kb} KB",
        "status": status,
        "scanned_on": scan_time
    })

    return render_template(
        "index.html",
        scanned=True,
        filename=filename,
        size=size_kb,
        status=status,
        total=total_files,
        clean=clean_files,
        threats=threats_found,
        scan_time=scan_time
    )

@app.route("/download_report", methods=["GET"])
def download_report():
    if not scan_history:
        return "No scan report available yet.", 404

    last = scan_history[-1]
    report = f"""
    SecureGuard Antivirus Report
    ----------------------------
    File: {last['file']}
    Size: {last['size']}
    Status: {last['status']}
    Scanned On: {last['scanned_on']}

    Total Files: 1
    Clean Files: {"1" if last['status']=="No Threats Found" else "0"}
    Threats Found: {"0" if last['status']=="No Threats Found" else "1"}

    SecureGuard Antivirus © 2025 | Developed by Balaji
    """
    buf = io.BytesIO(report.encode())
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="Scan_Report.txt", mimetype="text/plain")

@app.route("/history")
def history():
    return render_template("history.html", history=scan_history)

if __name__ == "__main__":
    app.run(debug=True)