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
- Processes and analyzes **2,500+ patient records** from the METABRIC dataset
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


from d3rlpy.algos import DiscreteCQL, DiscreteCQLConfig

