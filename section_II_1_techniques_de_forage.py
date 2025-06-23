import streamlit as st

st.markdown("## II. LES TECHNIQUES DE FORAGE")
st.write("")

# === PARAMÈTRES D'ENTRÉE ===
profondeur = st.number_input('Profondeur (m)', min_value=1.0, max_value=500.0, value=30.0, step=1.0)
type_sol = st.selectbox('Type de sol', ['sable', 'limon', 'argile', 'gravier', 'grès', 'basalte', 'calcaire', 'roche dure'])
niveau_eau = st.number_input("Niveau d'eau (m)", min_value=0.0, max_value=200.0, value=10.0, step=1.0)
usage = st.radio("Usage", ['Reconnaissance (piezométrie)', 'Exploitation (captage)'])
debit = st.slider("Débit (m³/h)", min_value=1.0, max_value=400.0, value=10.0, step=1.0)
qualite_eau = st.selectbox("Qualité eau", ['claire', 'chargée en sable', 'acide ou salée', 'sulfureuse ou gazeuse'])
stabilite_terrain = st.selectbox("Stabilité", ['stable', 'instable', 'inconnu'])
environnement = st.selectbox("Environnement", ['urbain', 'rural', 'zone exiguë', 'site isolé'])
hauteur_manometrique = st.number_input('HMT (m)', min_value=1.0, max_value=500.0, value=40.0, step=1.0)
rendement = st.slider("η (rendement)", min_value=0.3, max_value=0.9, value=0.65, step=0.01)
region = st.selectbox("Région", ["Zone sahélienne", "Forêt tropicale", "Montagne rocheuse", "Périphérie urbaine"])
type_tube = st.selectbox("Type de tube", ['PVC', 'Acier - terrain consolidé', 'Acier - terrain non consolidé'])
epaisseur = st.number_input("Épaisseur (mm)", min_value=1.0, max_value=50.0, value=10.0, step=1.0)
diametre = st.number_input("Diamètre (mm)", min_value=50.0, max_value=500.0, value=150.0, step=1.0)

# === TABLEAU DE RÉFÉRENCE DES DIAMÈTRES ===
table_diametres = [
    (10,  "3½ à 2", "5 à 6", "6", "8", "9⅝"),
    (30,  "2½ à 3", "6", "6 à 8", "9⅝", "10¾"),
    (50,  "3½ à 4", "8", "8", "9⅝", "10¾"),
    (100, "5 à 6", "9⅞ à 10", "8", "9⅝", "10¾"),
    (200, "7 à 8", "13 à 13⅞", "12", "14", "16"),
    (400, "9½ à 11", "18", "13", "16", "20"),
]

def get_alpha(tube_type, e, D):
    if tube_type == "PVC":
        return 26000
    elif tube_type == "Acier - terrain consolidé":
        return 2.5e6 if D/e > 50 else None
    elif tube_type == "Acier - terrain non consolidé":
        return 1.5e6 if D/e > 50 else None

if st.button("Lancer l'analyse"):
    rec = []

    # --- MÉTHODE DE FORAGE ---
    if profondeur < 30 and type_sol in ['sable', 'limon', 'argile'] and debit < 5:
        method = "Tarière manuelle ou battage léger"
    elif type_sol in ['grès', 'calcaire', 'basalte', 'roche dure']:
        method = "Marteau fond de trou à l’air"
    elif qualite_eau == 'chargée en sable':
        method = "Forage rotary avec crépine filtrante et gravier"
    else:
        method = "Forage rotary avec boue stabilisante"
    rec.append(f"🔧 Méthode de forage recommandée : {method}")

    # --- PRÉTUBAGE ---
    if stabilite_terrain == 'instable' or type_sol in ['sable', 'limon']:
        rec.append("🛡️ Prétubage recommandé : oui (stabilisation des premiers mètres)")

    # --- DIAMÈTRES ---
    for seuil, φ_crepine, φ_forage, φ_pompe, φ_tubage, φ_forage2 in table_diametres:
        if debit <= seuil:
            rec.append(f"📏 Débit ≤ {seuil} m³/h : Crépine {φ_crepine}, Forage {φ_forage}, Pompe {φ_pompe}, Tubage {φ_tubage}, Forage final {φ_forage2}")
            break

    # --- PUISSANCE ---
    Q = debit / 3600
    H = hauteur_manometrique
    eta = rendement
    puissance = (1000 * 9.81 * Q * H) / eta
    puissance_cv = puissance / 735.5
    rec.append(f"🔋 Puissance requise : {puissance:.1f} W ≈ {puissance_cv:.2f} CV")

    # --- ÉCRASEMENT ---
    alpha = get_alpha(type_tube, epaisseur, diametre)
    if alpha:
        P = alpha * (epaisseur / diametre) ** 3
        rec.append(f"🧮 Pression limite d’écrasement : {P:.2f} kg/cm²")
    else:
        rec.append("⚠️ D/e < 50 : α non applicable pour ce matériau.")

    # --- MATÉRIEL ---
    dispo = {
        "Zone sahélienne": "Tarière manuelle, pompe à corde, motopompe diesel",
        "Forêt tropicale": "Rotary hydraulique, pompe submersible, tube PVC renforcé",
        "Montagne rocheuse": "Marteau fond de trou, forage à air comprimé, crépine en acier",
        "Périphérie urbaine": "Forage motorisé sur camion, tubes acier, pompes électriques immergées"
    }
    rec.append(f"🧰 Matériel disponible en {region} : {dispo[region]}")

    # --- ENVIRONNEMENT ---
    if environnement in ['urbain', 'zone exiguë']:
        rec.append("🏙️ Choisir matériel compact, silencieux (marteau fond de trou, rotary léger)")
    else:
        rec.append("🌍 Aucune contrainte particulière sur l’encombrement")

    # === AFFICHAGE ===
    st.markdown("## 🔎 Résumé technique personnalisé")
    for r in rec:
        st.markdown(r)
