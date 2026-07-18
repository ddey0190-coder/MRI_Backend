from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)


CSV_FILE = os.path.join(os.path.dirname(__file__), "alzheimers_disease_data.csv")
print("Current Directory:", os.getcwd())
print("CSV Path:", os.path.abspath(CSV_FILE))

@app.route("/")
def home():
    return "MRI Backend is Running Successfully!"

@app.route("/summary")
def summary():
    df = pd.read_csv(CSV_FILE)

    return jsonify({
        "Total Rows": len(df),
        "Total Columns": len(df.columns),
        "Column Names": list(df.columns)
    })

@app.route("/stats")
def stats():
    try:
        df = pd.read_csv(CSV_FILE)

        return jsonify({
            "Columns": list(df.columns),
            "Gender Values": df["Gender"].unique().tolist(),
            "Diagnosis Values": df["Diagnosis"].unique().tolist()
        })

    except Exception as e:
        return jsonify({
            "Error": str(e)
        })
        
@app.route("/dashboard")
def dashboard():
    try:
        df = pd.read_csv(CSV_FILE)

        total_patients = len(df)
        male = len(df[df["Gender"] == 1])
        female = len(df[df["Gender"] == 0])

        alzheimers = len(df[df["Diagnosis"] == 1])
        healthy = len(df[df["Diagnosis"] == 0])

        average_age = round(df["Age"].mean(), 2)

        return jsonify({
            "total_patients": total_patients,
            "male": male,
            "female": female,
            "alzheimers": alzheimers,
            "healthy": healthy,
            "average_age": average_age
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })
        
@app.route("/patients")
def patients():
    df = pd.read_csv(CSV_FILE)

    data = df.head(10).to_dict(orient="records")

    return jsonify(data)

@app.route("/patient/<int:patient_id>")
def get_patient(patient_id):
    df = pd.read_csv(CSV_FILE)

    patient = df[df["PatientID"] == patient_id]

    if patient.empty:
        return jsonify({"message": "Patient Not Found"})

    return jsonify(patient.to_dict(orient="records")[0])

@app.route("/upload", methods=["GET","POST"])
def upload_file():

    if request.method == "GET":
        return "Upload API is Ready!"
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"})

    file.save(f"uploads/{file.filename}")

    return jsonify({
        "message": "File uploaded successfully!",
        "filename": file.filename
    })
    
@app.route("/age-analysis")
def age_analysis():
    try:
        df = pd.read_csv(CSV_FILE)

        age_groups = {
            "60-69": len(df[(df["Age"] >= 60) & (df["Age"] <= 69)]),
            "70-79": len(df[(df["Age"] >= 70) & (df["Age"] <= 79)]),
            "80-89": len(df[(df["Age"] >= 80) & (df["Age"] <= 89)]),
            "90+": len(df[df["Age"] >= 90])
        }

        return jsonify(age_groups)

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/gender-analysis")
def gender_analysis():
    try:
        df = pd.read_csv(CSV_FILE)

        male = len(df[df["Gender"] == 1])
        female = len(df[df["Gender"] == 0])

        return jsonify({
            "Male": male,
            "Female": female
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/disease-analysis")
def disease_analysis():
    try:
        df = pd.read_csv(CSV_FILE)

        alzheimers = len(df[df["Diagnosis"] == 1])
        healthy = len(df[df["Diagnosis"] == 0])

        return jsonify({
            "Alzheimers": alzheimers,
            "Healthy": healthy
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/patient/<int:patient_id>")
def patient(patient_id):
    try:
        df = pd.read_csv(CSV_FILE)

        result = df[df["PatientID"] == patient_id]

        if result.empty:
            return jsonify({"message": "Patient not found"})

        return jsonify(result.to_dict(orient="records")[0])

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/search")
def search():
    try:
        name = request.args.get("name")

        df = pd.read_csv(CSV_FILE)

        if not name:
            return jsonify({"error": "Please provide a name"})

        result = df[df["DoctorInCharge"].str.contains(name, case=False, na=False)]

        return jsonify(result.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/risk-analysis")
def risk_analysis():
    try:
        df = pd.read_csv(CSV_FILE)

        high_risk = len(df[(df["Age"] >= 80) & (df["Diagnosis"] == 1)])
        low_risk = len(df[(df["Age"] < 80) & (df["Diagnosis"] == 0)])

        return jsonify({
            "High Risk": high_risk,
            "Low Risk": low_risk
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)