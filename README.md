# 🧠 Offline Reinforcement Learning for Breast Cancer Treatment Optimization

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-Frontend-blue.svg)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-Latest-brightgreen.svg)](https://nodejs.org/)
[![d3rlpy](https://img.shields.io/badge/d3rlpy-Offline_RL-orange.svg)](https://github.com/takuseno/d3rlpy)

---

## 📌 Project Overview
Offline-RL-METABRIC-Dataset applies Offline Reinforcement Learning using the METABRIC breast cancer dataset to optimize treatment strategies. Implements Conservative Q-Learning (CQL) with d3rlpy, modeling clinical features as states, treatments as actions, and survival outcomes as rewards for better therapy recommendations. This project investigates the use of **Offline Reinforcement Learning (RL)** techniques to optimize **personalized breast cancer treatment decisions** using the **METABRIC clinical dataset**.  

The system frames the clinical decision-making process as a **Markov Decision Process (MDP)**:
- **States** → Patient clinical features (e.g., tumor size, receptor status, age)
- **Actions** → Treatment strategies (e.g., chemotherapy, hormone therapy, radiotherapy)
- **Rewards** → Survival outcomes and recurrence rates

By leveraging **historical patient data**, we develop a **data-driven, interpretable RL model** that provides **personalized treatment recommendations** while ensuring patient safety by avoiding live experimentation.

---

## 🧠 Key Features
- Implementation of **Offline Reinforcement Learning** using **d3rlpy**
- Utilizes **Discrete Conservative Q-Learning (CQL)** algorithm
- Processes and analyzes **25,000+ patient records** from the METABRIC dataset
- **Flask API** for backend model inference and integration
- **ReactJS** frontend for interactive visualization and prediction results
- Ensures **model reproducibility, interpretability, and clinical relevance**

---

## 🛠️ Tech Stack

### **Languages & Frameworks**
- **Python 3.12+** → Machine Learning, Data Processing & RL Modeling
- **Flask** → Backend REST API
- **ReactJS** → Frontend Interface
- **Node.js (Latest)** → Required for React Development Server


# ⚡ Installation & Setup

Follow the steps below to set up and run the **Offline Reinforcement Learning for Breast Cancer Treatment Optimization** project on your local machine.

---

## **1. Prerequisites**

Before you begin, make sure you have the following installed:

* **Node.js** (Latest version) → [Download here](https://nodejs.org/)
* **Python 3.12+** → [Download here](https://www.python.org/)
* **pip** → Comes with Python 3.12+
* **Git** → [Download here](https://git-scm.com/)

---

## **2. Clone the Repository**

```bash
git clone https://github.com/thejasramappa/Offline-RL-METABRIC-Dataset.git
cd Offline-RL-METABRIC-Dataset
```

---

## **3. Setup Frontend (ReactJS)**

Open a terminal and run:

```bash
cd frontend
npm install
npm start
```

* Installs all frontend dependencies.
* Starts React app on **[http://localhost:3000](http://localhost:3000)**.

---

## **4. Setup Backend (Flask API)**

Open a **new terminal** and run:

```bash
cd backend
pip install -r requirements.txt
python server.py
```

* Installs Python dependencies.
* Starts Flask API on **[http://localhost:5000](http://localhost:5000)**.

---

## **5. Running the Application**

1. Start the **backend server**:

   ```bash
   cd backend
   python server.py
   ```
2. Start the **frontend server**:

   ```bash
   cd frontend
   npm start
   ```
3. Open your browser → **[http://localhost:3000](http://localhost:3000)**

---

## **6. Folder Structure**

```
Offline-RL-METABRIC-Dataset/
│── frontend/           # ReactJS frontend
│   ├── public/
│   ├── src/
│   └── package.json
│
│── backend/            # Flask backend
│   ├── server.py       # Flask app entry point
│   ├── model.pkl       # Trained RL model
│   ├── requirements.txt
│
│── data/               # METABRIC dataset (not included)
│── README.md
```

---

## **7. Important Notes**

* Use **Python 3.12** for compatibility.
* Use **latest Node.js** for React setup.
* Always start **backend** first, then **frontend**.
* **Dataset** is not included due to privacy constraints.

---

## **8. Troubleshooting**

| Issue                           | Solution                                                         |
| ------------------------------- | ---------------------------------------------------------------- |
| `npm start` not working         | Delete `node_modules` + `package-lock.json` → run `npm install`. |
| `ModuleNotFoundError` in Python | Run `pip install -r requirements.txt`.                           |
| Flask server error              | Use **Python 3.12** and check `server.py`.                       |
| Blank React screen              | Stop server (`Ctrl+C`) → run `npm start` again.                  |

---

## **9. API Endpoints**

**Base URL:** `http://localhost:5000`

| Endpoint   | Method | Description                   |
| ---------- | ------ | ----------------------------- |
| `/predict` | POST   | Get treatment recommendations |
| `/train`   | POST   | Train RL model on dataset     |
| `/status`  | GET    | Check backend API health      |

---

## **10. Next Steps**

* Load your patient data via the UI.
* Explore personalized treatment recommendations.
* Extend support for new datasets and RL algorithms.

---

## **11. Contact**

**Author**: Thejas Ramappa
📌 MSc Information Technology
📩 For any queries, open an **issue** or reach out via **GitHub**.

---



