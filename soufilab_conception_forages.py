import streamlit as st

st.set_page_config(page_title="SoufiLab Conception Forages", layout="wide")

st.title("SoufiLab – Conception d'Ouvrages de Forage")

st.markdown("""
Bienvenue dans l'application **SoufiLab_Conception_forages**.  
Choisissez une section dans le menu latéral pour démarrer l’analyse technique.
""")

# === Menu de navigation ===
sections = {
    "I. Exploration des eaux souterraines": "section_I_exploration_eaux_souterraines",
    "II. Techniques de forage": "section_II_1_techniques_de_forage",
    "II. Techniques de forage – Facturation": "section_II_2_technique_de_forage_facturation",
    "III. Équipement et mise en production": "section_III_equipement_et_mise_en_production",
    "IV.1.1. Essais par paliers (transitoire)": "section_IV_1_1_essais_par_paliers",
    "IV.1.2. Essais longue durée (transitoire)": "section_IV_1_2_essais_longue_duree",
    "IV.2. Régime permanent": "section_IV_2_regime_permanent"
}

choice = st.sidebar.radio("📘 Naviguer entre les sections :", list(sections.keys()))

# Importation dynamique (chaque section dans un fichier séparé)
with st.spinner("Chargement de la section..."):
    exec(open(f"{sections[choice]}.py", encoding="utf-8").read())
