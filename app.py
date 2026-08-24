import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, rdFingerprintGenerator
import numpy as np
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

st.set_page_config(page_title="AI Molecule Dashboard", page_icon="🧪", layout="centered")

# ---------- Custom styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #F4FAF9;
}
.header-box {
    background: #0B2E33;
    border-radius: 18px;
    padding: 2rem 1.8rem;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: 2.6rem;
    color: #FFFFFF;
    margin-bottom: 0.3rem;
}
.hero-sub {
    color: #9FC7C2;
    font-size: 1.05rem;
    margin: 0;
}
.section-label {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: #028090;
    letter-spacing: 1.5px;
    font-size: 0.8rem;
    text-transform: uppercase;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}
div.stButton > button {
    background-color: #FFFFFF;
    color: #0B2E33;
    border: 2px solid #02C39A;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    background-color: #02C39A;
    color: #FFFFFF;
    border-color: #02C39A;
}
.result-card {
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.result-good { background-color: #E3F6F0; border-left: 6px solid #02C39A; }
.result-bad  { background-color: #FDEDEC; border-left: 6px solid #E74C3C; }
.result-warn { background-color: #FFF7E0; border-left: 6px solid #F1B60A; }
.result-label {
    font-size: 0.85rem;
    color: #5C6B6C;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.result-value {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0B2E33;
    margin-top: 0.2rem;
}
.mol-frame {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 1.2rem;
}
.mol-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #0B2E33;
    margin-bottom: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- Model loading ----------
@st.cache_resource
def load_models():
    morgan_gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=1024)

    def get_fingerprint(smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        return np.array(morgan_gen.GetFingerprint(mol))

    tox_url = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/tox21.csv.gz"
    tox_df = pd.read_csv(tox_url)
    tox_data = tox_df[['smiles', 'SR-p53']].dropna()
    tox_data['fingerprint'] = tox_data['smiles'].apply(get_fingerprint)
    tox_data = tox_data.dropna(subset=['fingerprint'])
    X_tox = np.array(tox_data['fingerprint'].tolist())
    y_tox = tox_data['SR-p53'].values
    tox_model = RandomForestClassifier(n_estimators=100, random_state=42)
    tox_model.fit(X_tox, y_tox)

    esol_url = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/delaney-processed.csv"
    esol_df = pd.read_csv(esol_url)
    esol_data = esol_df[['smiles', 'measured log solubility in mols per litre']].dropna()
    esol_data.columns = ['smiles', 'solubility']
    esol_data['fingerprint'] = esol_data['smiles'].apply(get_fingerprint)
    esol_data = esol_data.dropna(subset=['fingerprint'])
    X_sol = np.array(esol_data['fingerprint'].tolist())
    y_sol = esol_data['solubility'].values
    sol_model = RandomForestRegressor(n_estimators=100, random_state=42)
    sol_model.fit(X_sol, y_sol)

    return morgan_gen, tox_model, sol_model

def check_lipinski(mol):
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    h_donors = Descriptors.NumHDonors(mol)
    h_acceptors = Descriptors.NumHAcceptors(mol)
    violations = sum([mw > 500, logp > 5, h_donors > 5, h_acceptors > 10])
    if violations == 0:
        return "Drug-like", "✅", "result-good"
    else:
        return f"Risky ({violations} rule violated)", "⚠️", "result-warn"

@st.cache_data
def get_molecule_name(smiles):
    known_names = {
        "CC(=O)OC1=CC=CC=C1C(=O)O": "Aspirin",
        "CN1C=NC2=C1C(=O)N(C(=O)N2C)C": "Caffeine",
        "CC(=O)NC1=CC=C(C=C1)O": "Paracetamol",
        "c1ccccc1": "Benzene",
    }
    if smiles in known_names:
        return known_names[smiles]
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/synonyms/JSON"
        response = requests.get(url, timeout=5)
        data = response.json()
        name = data["InformationList"]["Information"][0]["Synonym"][0]
        return name.title()
    except Exception:
        return "Unknown Molecule"

# ---------- Header ----------
st.markdown("""
<div class="header-box">
    <div class="hero-title">🧪 AI Molecule Multi-Predictor</div>
    <div class="hero-sub">AI in Chemistry — Toxicity, Solubility &amp; Drug-Likeness, screened in seconds</div>
</div>
""", unsafe_allow_html=True)

with st.spinner("Loading models... (first run takes ~1 minute)"):
    morgan_gen, tox_model, sol_model = load_models()

# ---------- Examples ----------
st.markdown('<div class="section-label">Try an example</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
example = None
if col1.button("💊 Aspirin"): example = "CC(=O)OC1=CC=CC=C1C(=O)O"
if col2.button("☕ Caffeine"): example = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
if col3.button("🩹 Paracetamol"): example = "CC(=O)NC1=CC=C(C=C1)O"
if col4.button("⬡ Benzene"): example = "c1ccccc1"

st.markdown('<div class="section-label">Or enter a SMILES code</div>', unsafe_allow_html=True)
smiles_input = st.text_input("", value=example if example else "", placeholder="e.g. CC(=O)OC1=CC=CC=C1C(=O)O", label_visibility="collapsed")

# ---------- Results ----------
if smiles_input:
    mol = Chem.MolFromSmiles(smiles_input)
    if mol is None:
        st.error("Invalid SMILES code — please check and try again.")
    else:
        molecule_name = get_molecule_name(smiles_input)

        st.markdown('<div class="mol-frame">', unsafe_allow_html=True)
        st.markdown(f'<div class="mol-name">{molecule_name}</div>', unsafe_allow_html=True)
        st.image(Draw.MolToImage(mol, size=(320, 320)))
        st.markdown('</div>', unsafe_allow_html=True)

        fp = np.array(morgan_gen.GetFingerprint(mol)).reshape(1, -1)

        lip_text, lip_icon, lip_class = check_lipinski(mol)

        tox_pred = tox_model.predict(fp)[0]
        tox_prob = tox_model.predict_proba(fp)[0][1]
        if tox_pred == 1:
            tox_text, tox_icon, tox_class = f"Toxic ({tox_prob:.0%} confidence)", "⚠️", "result-bad"
        else:
            tox_text, tox_icon, tox_class = f"Non-Toxic ({(1-tox_prob):.0%} confidence)", "✅", "result-good"

        sol_pred = sol_model.predict(fp)[0]
        if sol_pred > -2:
            sol_text, sol_icon, sol_class = f"Good solubility ({sol_pred:.2f})", "✅", "result-good"
        else:
            sol_text, sol_icon, sol_class = f"Poor solubility ({sol_pred:.2f})", "⚠️", "result-warn"

        for label, value, icon, css_class in [
            ("Drug-Likeness", lip_text, lip_icon, lip_class),
            ("Toxicity", tox_text, tox_icon, tox_class),
            ("Solubility", sol_text, sol_icon, sol_class),
        ]:
            st.markdown(f"""
            <div class="result-card {css_class}">
                <div>
                    <div class="result-label">{label}</div>
                    <div class="result-value">{value}</div>
                </div>
                <div style="font-size:1.8rem;">{icon}</div>
            </div>
            """, unsafe_allow_html=True)
