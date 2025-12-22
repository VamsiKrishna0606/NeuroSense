from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os, uuid

from model.inference import run_prediction
from utils.report import generate_report

# ---------------------------------
# Setup
# ---------------------------------
app = Flask(__name__)
CORS(app)

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# ---------------------------------
# 1️⃣ Upload EEG file
# ---------------------------------
@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_id = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_id)
    file.save(file_path)

    return jsonify({"fileId": file_id})


# ---------------------------------
# 2️⃣ Run prediction (CALLS PYTORCH MODEL)
# ---------------------------------
@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    file_id = data.get("fileId")

    file_path = os.path.join(UPLOAD_DIR, file_id)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # 🔥 Call your Brain2Vec model
    result = run_prediction(file_path)

    # 🔥 Generate PDF report
    generate_report(file_id, result)

    return jsonify(result)


# ---------------------------------
# 3️⃣ Download report
# ---------------------------------
@app.route("/api/report/<file_id>", methods=["GET"])
def download_report(file_id):
    report_path = os.path.join(REPORT_DIR, f"{file_id}.pdf")
    if not os.path.exists(report_path):
        return jsonify({"error": "Report not ready"}), 404

    return send_file(report_path, as_attachment=True)


# ---------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
