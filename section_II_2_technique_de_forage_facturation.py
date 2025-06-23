import streamlit as st

st.markdown("## II. Technique de forage – Facturation")

# === Paramètres d'entrée ===
profondeur = st.number_input("Profondeur (m)", min_value=1.0, max_value=1000.0, value=50.0, step=1.0)
vitesse = st.slider("Vitesse (m/j)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
region_tarifs = {
    "Zone sahélienne": 90,
    "Forêt tropicale": 130,
    "Montagne rocheuse": 170,
    "Périphérie urbaine": 150
}
region = st.selectbox("Région (€/m)", list(region_tarifs.keys()))
tarif_region = region_tarifs[region]

monnaies = {"Euro (€)": "€", "Dollar ($)": "$", "Franc CFA (FCFA)": "FCFA"}
monnaie_label = st.selectbox("Monnaie", list(monnaies.keys()))
monnaie_symbole = monnaies[monnaie_label]

# === Calculs ===
if st.button("Simuler le chantier"):
    duree = profondeur / vitesse
    cout_total = profondeur * tarif_region

    st.markdown("## 🏗️ Simulation de chantier")
    st.markdown(f"""
- 📍 **Profondeur** : {profondeur} m  
- 🚜 **Vitesse de forage** : {vitesse} m/jour  
- 🗺️ **Coût unitaire régional** : {tarif_region} {monnaie_symbole}/m  
- 💰 **Coût total estimé** : **{cout_total:,.0f} {monnaie_symbole}**  
- ⏱️ **Durée estimée** : **{duree:.1f} jours**  

> Montant exprimé en **{monnaie_label}**
""")
