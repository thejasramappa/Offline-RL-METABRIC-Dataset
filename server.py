from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import os
import re
import pandas as pd  # added

app = Flask(__name__)
CORS(app)

MEASURE_CONFIDENCE_HORMONE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/measure_model_confidence_hormone.py'))
MEASURE_CONFIDENCE_RADIO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/measure_model_confidence_radio.py'))
MEASURE_CONFIDENCE_CHEMO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/measure_model_confidence_chemo.py'))
MEASURE_CONFIDENCE_ALL_TREATMENT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/measure_model_confidence_all.py'))

ALL_PREDICT_SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/live_predict_all_treatment.py'))
CHEMO_PREDICT_SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/live_predict_chemo.py'))
RADIO_PREDICT_SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/live_predict_radio.py'))
HORMONE_PREDICT_SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/live_predict_hormone.py'))

SCRIPTS_DIR = os.path.dirname(CHEMO_PREDICT_SCRIPT_PATH)

# New: data directory and log file map
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
LOG_FILES = {
    "all": os.path.join(DATA_DIR, "live_predict_all_log.csv"),
    "chemo": os.path.join(DATA_DIR, "live_predictions_chemo_log.csv"),
    "radio": os.path.join(DATA_DIR, "live_predictions_radio_log.csv"),
    "hormone": os.path.join(DATA_DIR, "live_predictions_hormone_log.csv"),
}

# New: generic logs endpoint
@app.route('/logs/<log_type>', methods=['GET'])
def get_logs(log_type: str):
    path = LOG_FILES.get(log_type.lower())
    if not path:
        return jsonify({'error': 'Unknown log type'}), 400
    if not os.path.exists(path):
        return jsonify({'rows': []})
    try:
        df = pd.read_csv(path)
        rows = df.to_dict(orient='records')
        return jsonify({'rows': rows})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/measure_model_confidence_all', methods=['GET'])
def measure_model_confidence_all():
    try:
        result = subprocess.run(
            [sys.executable, MEASURE_CONFIDENCE_ALL_TREATMENT],
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR
        )
        match = re.search(r'Approximate Model Confidence \(Softmax %\): ([\d.]+ ?%)', result.stdout)
        confidence_value = match.group(1).strip() if match else "N/A"
        return jsonify({'confidence': confidence_value})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/measure_model_confidence_chemo', methods=['GET'])
def measure_model_confidence_chemo():
    try:
        result = subprocess.run(
            [sys.executable, MEASURE_CONFIDENCE_CHEMO],
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR
        )
        match = re.search(r'Approximate Model Confidence \(Softmax %\): ([\d.]+ ?%)', result.stdout)
        confidence_value = match.group(1).strip() if match else "N/A"
        return jsonify({'confidence': confidence_value})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/measure_model_confidence_radio', methods=['GET'])
def measure_model_confidence_radio():
    try:
        result = subprocess.run(
            [sys.executable, MEASURE_CONFIDENCE_RADIO],
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR
        )
        match = re.search(r'Approximate Model Confidence \(Softmax %\): ([\d.]+ ?%)', result.stdout)
        confidence_value = match.group(1).strip() if match else "N/A"
        return jsonify({'confidence': confidence_value})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/measure_model_confidence_hormone', methods=['GET'])
def measure_model_confidence_hormone():
    try:
        result = subprocess.run(
            [sys.executable, MEASURE_CONFIDENCE_HORMONE],
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR
        )
        match = re.search(r'Approximate Model Confidence \(Softmax %\): ([\d.]+ ?%)', result.stdout)
        confidence_value = match.group(1).strip() if match else "N/A"
        return jsonify({'confidence': confidence_value})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_all', methods=['POST'])
def predict_all():
    try:
        data = request.get_json(force=True)
        print("Received input data:", data)

        args = [
            str(data.get('id', '')),
            str(data.get('patient_name', '')),
            str(data.get('age', '')),
            str(data.get('tumor_size', '')),
            str(data.get('grade', '')),
            str(data.get('er', '')),
            str(data.get('pr', '')),
            str(data.get('her2', ''))
        ]

        # Run live_predict.py with CLI args
        result = subprocess.run(
            [sys.executable, ALL_PREDICT_SCRIPT_PATH] + args,
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR,
            timeout=120  # prevent indefinite hangs
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        print("live_predict.py stdout:", stdout)
        if stderr:
            print("live_predict.py stderr:", stderr)

        if result.returncode != 0:
            return jsonify({'error': 'Prediction script failed', 'details': stderr or stdout}), 500

        match = re.search(r'Prediction:\s*(.+)', stdout)
        if match:
            prediction_msg = match.group(1).strip()
            return jsonify({'result': prediction_msg})
        else:
            return jsonify({'error': 'Could not parse prediction output', 'details': stdout}), 500

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Prediction timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/predict_chemo', methods=['POST'])
def predict_chemo():
    try:
        data = request.get_json(force=True)
        print("Received input data:", data)

        args = [
            str(data.get('id', '')),
            str(data.get('patient_name', '')),
            str(data.get('age', '')),
            str(data.get('tumor_size', '')),
            str(data.get('grade', '')),
            str(data.get('er', '')),
            str(data.get('pr', '')),
            str(data.get('her2', ''))
        ]

        # Run live_predict.py with CLI args
        result = subprocess.run(
            [sys.executable, CHEMO_PREDICT_SCRIPT_PATH] + args,
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR,
            timeout=120  # prevent indefinite hangs
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        print("live_predict.py stdout:", stdout)
        if stderr:
            print("live_predict.py stderr:", stderr)

        if result.returncode != 0:
            return jsonify({'error': 'Prediction script failed', 'details': stderr or stdout}), 500

        match = re.search(r'Prediction:\s*(.+)', stdout)
        if match:
            prediction_msg = match.group(1).strip()
            return jsonify({'result': prediction_msg})
        else:
            return jsonify({'error': 'Could not parse prediction output', 'details': stdout}), 500

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Prediction timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict_radio', methods=['POST'])
def predict_radio():
    try:
        data = request.get_json(force=True)
        print("Received input data:", data)

        args = [
              str(data.get('id', '')),
            str(data.get('patient_name', '')),
            str(data.get('age', '')),
            str(data.get('tumor_size', '')),
            str(data.get('grade', '')),
            str(data.get('er', '')),
            str(data.get('pr', '')),
            str(data.get('her2', ''))
        ]

        # Run live_predict.py with CLI args
        result = subprocess.run(
            [sys.executable, RADIO_PREDICT_SCRIPT_PATH] + args,
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR,
            timeout=120  # prevent indefinite hangs
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        print("live_predict.py stdout:", stdout)
        if stderr:
            print("live_predict.py stderr:", stderr)

        if result.returncode != 0:
            return jsonify({'error': 'Prediction script failed', 'details': stderr or stdout}), 500

        match = re.search(r'Prediction:\s*(.+)', stdout)
        if match:
            prediction_msg = match.group(1).strip()
            return jsonify({'result': prediction_msg})
        else:
            return jsonify({'error': 'Could not parse prediction output', 'details': stdout}), 500

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Prediction timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict_hormone', methods=['POST'])
def predict_hormone():
    try:
        data = request.get_json(force=True)
        print("Received input data:", data)

        args = [
            str(data.get('id', '')),
            str(data.get('patient_name', '')),
            str(data.get('age', '')),
            str(data.get('tumor_size', '')),
            str(data.get('grade', '')),
            str(data.get('er', '')),
            str(data.get('pr', '')),
            str(data.get('her2', ''))
        ]

        # Run live_predict.py with CLI args
        result = subprocess.run(
            [sys.executable, HORMONE_PREDICT_SCRIPT_PATH] + args,
            capture_output=True,
            text=True,
            cwd=SCRIPTS_DIR,
            timeout=120  # prevent indefinite hangs
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        print("live_predict.py stdout:", stdout)
        if stderr:
            print("live_predict.py stderr:", stderr)

        if result.returncode != 0:
            return jsonify({'error': 'Prediction script failed', 'details': stderr or stdout}), 500

        match = re.search(r'Prediction:\s*(.+)', stdout)
        if match:
            prediction_msg = match.group(1).strip()
            return jsonify({'result': prediction_msg})
        else:
            return jsonify({'error': 'Could not parse prediction output', 'details': stdout}), 500

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Prediction timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Bind to localhost:5000
    app.run(host='0.0.0.0', port=5000, debug=True)
