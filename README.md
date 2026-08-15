# 🧪 AI Molecule Multi-Predictor Dashboard

An AI-powered web application for analyzing molecules and providing multiple chemistry and drug-discovery related predictions from a single molecule input.

The dashboard combines cheminformatics, machine learning, and chemical property analysis into one simple and interactive interface.

---

## 🚀 Project Overview

Evaluating a molecule for potential drug-related properties can involve multiple computational and laboratory-based steps.

This project provides a preliminary computational analysis of a molecule by combining:

- Molecular structure visualization
- Drug-likeness analysis
- Toxicity prediction
- Aqueous solubility prediction
- Molecular name identification

The application is designed as an educational and exploratory tool to demonstrate how **Artificial Intelligence and Chemistry can work together in early-stage molecular analysis.**

> ⚠️ This application provides computational predictions and is not intended to replace laboratory experiments, clinical testing, or professional medical advice.

---

## ✨ Features

### 🧬 1. Molecular Structure Visualization

Enter a molecule using its **SMILES (Simplified Molecular Input Line Entry System)** notation.

The application uses **RDKit** to generate and display the corresponding 2D molecular structure.

Example molecules include:

- Aspirin
- Caffeine
- Paracetamol
- Benzene

---

### 💊 2. Drug-Likeness Analysis

The application evaluates the molecule using **Lipinski's Rule of Five**.

The following properties are calculated using RDKit:

- Molecular Weight
- LogP
- Hydrogen Bond Donors
- Hydrogen Bond Acceptors

Based on these properties, the application provides a preliminary drug-likeness assessment.

---

### ☠️ 3. Toxicity Prediction

A **Random Forest Classifier** is used to predict toxicity-related activity.

The model is trained using the **Tox21 dataset**, focusing specifically on the **SR-p53 toxicity pathway**.

The dashboard presents the model's prediction in an easy-to-understand format.

---

### 💧 4. Solubility Prediction

A **Random Forest Regressor** is used to estimate molecular solubility.

The model is trained using the **ESOL (Delaney) dataset**.

The predicted solubility value is presented to help understand the molecule's estimated aqueous solubility.

---

### 🔎 5. Molecular Name Identification

The application attempts to identify the common name of a molecule using the **PubChem API**.

A manual fallback dictionary is also included for commonly used molecules such as:

- Aspirin
- Caffeine
- Paracetamol
- Benzene

---

## 🧠 Machine Learning Models

| Prediction | Dataset | Model | Output |
|---|---|---|---|
| Toxicity | Tox21 | Random Forest Classifier | Toxicity prediction |
| Solubility | ESOL / Delaney | Random Forest Regressor | Predicted solubility |
| Drug-likeness | RDKit calculations | Lipinski Rule of Five | Drug-likeness assessment |

### Toxicity Model

- Dataset: Tox21
- Target: SR-p53 toxicity pathway
- Algorithm: Random Forest Classifier

### Solubility Model

- Dataset: ESOL / Delaney
- Algorithm: Random Forest Regressor

---

## 🛠️ Technology Stack

### Programming Language
- Python

### Chemistry & Cheminformatics
- RDKit

### Machine Learning
- scikit-learn
- Random Forest Classifier
- Random Forest Regressor

### Data Processing
- pandas
- NumPy

### Web Application
- Streamlit

### External API
- PubChem API

### Development Environment
- Google Colab

### Deployment
- Streamlit Community Cloud

---

## 📊 Datasets

### Tox21 Dataset

The Tox21 dataset is used for toxicity-related machine learning.

The project focuses on the SR-p53 toxicity pathway for the classification task.

### ESOL / Delaney Dataset

The ESOL dataset is used to train the molecular solubility prediction model.

The datasets were obtained from publicly available DeepChem resources.

---

## 🔄 Application Workflow

```text
User enters SMILES
        ↓
   RDKit parsing
        ↓
Molecular structure generated
        ↓
 ┌───────────────┬────────────────┬─────────────────┐
 ↓               ↓                ↓
Drug-likeness  Toxicity       Solubility
Analysis       Prediction     Prediction
 ↓               ↓                ↓
Lipinski       Random Forest   Random Forest
Properties     Classifier      Regressor
 └───────────────┴────────────────┴─────────────────┘
                       ↓
              Molecular name lookup
                       ↓
              Combined result dashboard# 🧪 AI Molecule Multi-Predictor Dashboard

An AI-powered web application for analyzing molecules and providing multiple chemistry and drug-discovery related predictions from a single molecule input.

The dashboard combines cheminformatics, machine learning, and chemical property analysis into one simple and interactive interface.

---

## 🚀 Project Overview

Evaluating a molecule for potential drug-related properties can involve multiple computational and laboratory-based steps.

This project provides a preliminary computational analysis of a molecule by combining:

- Molecular structure visualization
- Drug-likeness analysis
- Toxicity prediction
- Aqueous solubility prediction
- Molecular name identification

The application is designed as an educational and exploratory tool to demonstrate how **Artificial Intelligence and Chemistry can work together in early-stage molecular analysis.**

> ⚠️ This application provides computational predictions and is not intended to replace laboratory experiments, clinical testing, or professional medical advice.

---

## ✨ Features

### 🧬 1. Molecular Structure Visualization

Enter a molecule using its **SMILES (Simplified Molecular Input Line Entry System)** notation.

The application uses **RDKit** to generate and display the corresponding 2D molecular structure.

Example molecules include:

- Aspirin
- Caffeine
- Paracetamol
- Benzene

---

### 💊 2. Drug-Likeness Analysis

The application evaluates the molecule using **Lipinski's Rule of Five**.

The following properties are calculated using RDKit:

- Molecular Weight
- LogP
- Hydrogen Bond Donors
- Hydrogen Bond Acceptors

Based on these properties, the application provides a preliminary drug-likeness assessment.

---

### ☠️ 3. Toxicity Prediction

A **Random Forest Classifier** is used to predict toxicity-related activity.

The model is trained using the **Tox21 dataset**, focusing specifically on the **SR-p53 toxicity pathway**.

The dashboard presents the model's prediction in an easy-to-understand format.

---

### 💧 4. Solubility Prediction

A **Random Forest Regressor** is used to estimate molecular solubility.

The model is trained using the **ESOL (Delaney) dataset**.

The predicted solubility value is presented to help understand the molecule's estimated aqueous solubility.

---

### 🔎 5. Molecular Name Identification

The application attempts to identify the common name of a molecule using the **PubChem API**.

A manual fallback dictionary is also included for commonly used molecules such as:

- Aspirin
- Caffeine
- Paracetamol
- Benzene

---

## 🧠 Machine Learning Models

| Prediction | Dataset | Model | Output |
|---|---|---|---|
| Toxicity | Tox21 | Random Forest Classifier | Toxicity prediction |
| Solubility | ESOL / Delaney | Random Forest Regressor | Predicted solubility |
| Drug-likeness | RDKit calculations | Lipinski Rule of Five | Drug-likeness assessment |

### Toxicity Model

- Dataset: Tox21
- Target: SR-p53 toxicity pathway
- Algorithm: Random Forest Classifier

### Solubility Model

- Dataset: ESOL / Delaney
- Algorithm: Random Forest Regressor

---

## 🛠️ Technology Stack

### Programming Language
- Python

### Chemistry & Cheminformatics
- RDKit

### Machine Learning
- scikit-learn
- Random Forest Classifier
- Random Forest Regressor

### Data Processing
- pandas
- NumPy

### Web Application
- Streamlit

### External API
- PubChem API

### Development Environment
- Google Colab

### Deployment
- Streamlit Community Cloud

---

## 📊 Datasets

### Tox21 Dataset

The Tox21 dataset is used for toxicity-related machine learning.

The project focuses on the SR-p53 toxicity pathway for the classification task.

### ESOL / Delaney Dataset

The ESOL dataset is used to train the molecular solubility prediction model.

The datasets were obtained from publicly available DeepChem resources.

---

## 🔄 Application Workflow

```text
User enters SMILES
        ↓
   RDKit parsing
        ↓
Molecular structure generated
        ↓
 ┌───────────────┬────────────────┬─────────────────┐
 ↓               ↓                ↓
Drug-likeness  Toxicity       Solubility
Analysis       Prediction     Prediction
 ↓               ↓                ↓
Lipinski       Random Forest   Random Forest
Properties     Classifier      Regressor
 └───────────────┴────────────────┴─────────────────┘
                       ↓
              Molecular name lookup
                       ↓
              Combined result dashboard
