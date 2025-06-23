import streamlit as st

st.markdown("## III. EQUIPEMENT ET MISE EN PRODUCTION D'UN FORAGE")

# === MENU ===
menu_option = st.selectbox("Choisir une étape :", [
    "1️⃣ Colonne de captage",
    "2️⃣ Gravier filtrant",
    "3️⃣ Cimentation",
    "4️⃣ Nettoyage",
    "5️⃣ Développement"
])

# === ÉTAPE 1 : Colonne de captage ===
if menu_option == "1️⃣ Colonne de captage":
    st.markdown("### 🔩 Mise en place de la colonne de captage")
    tube_diametre = st.number_input("Ø tube (mm)", value=150.0)
    hauteur_crepine = st.number_input("H crépine (m)", value=6.0)
    coeff_ouverture = st.slider("C (%)", min_value=10, max_value=40, value=20)
    if st.button("Calculer le débit"):
        C = coeff_ouverture / 100
        phi = tube_diametre / 1000
        q = 3.4 * phi * C
        debit_total = q * hauteur_crepine
        st.write(f"🔹 Débit admissible par mètre linéaire : {q:.2f} m³/h/m")
        st.write(f"🔹 Débit total pour {hauteur_crepine} m : {debit_total:.2f} m³/h")

# === ÉTAPE 2 : Gravier filtrant ===
elif menu_option == "2️⃣ Gravier filtrant":
    st.markdown("### 🪨 Mise en place du massif de gravier filtrant")
    D_hole = st.number_input("Ø trou (pouce)", value=8.0)
    D_tube = st.number_input("Ø tube (pouce)", value=6.0)
    h_gravier = st.number_input("Hauteur gravier (m)", value=10.0)
    if st.button("Calculer volume de gravier"):
        V = 0.28 * h_gravier * (D_hole**2 - D_tube**2)
        st.write(f"🔹 Volume théorique de gravier : {V:.2f} litres")

# === ÉTAPE 3 : Cimentation ===
elif menu_option == "3️⃣ Cimentation":
    st.markdown("### 🧱 Cimentation")
    eau = st.number_input("Eau (L)", value=50.0)
    ciment = st.number_input("Ciment (kg)", value=100.0)
    if st.button("Calculer le volume de laitier"):
        laitier = eau + ciment * 0.25
        st.write(f"🔹 Volume de laitier produit : {laitier:.2f} litres")

# === ÉTAPE 4 : Nettoyage ===
elif menu_option == "4️⃣ Nettoyage":
    st.markdown("### 💧 Nettoyage du forage")
    st.write("🔹 Rincer à l’eau claire pour éliminer le cake.")
    st.write("🔹 Alterner rinçage et pompage air-lift jusqu’à obtention d’une eau claire.")

# === ÉTAPE 5 : Développement ===
elif menu_option == "5️⃣ Développement":
    st.markdown("### 🚿 Développement du forage")
    methode = st.selectbox("Méthode :", [
        "Surpompage", "Pompage alterné", "Pompage localisé", "Pistonnage",
        "Jet haute pression", "Air lift", "Traitement chimique"
    ])
    if st.button("Afficher méthode"):
        dico = {
            "Surpompage": "Pompage en paliers successifs (1,5 à 2× Q exploitation).",
            "Pompage alterné": "Arrêts brusques pour mobiliser les fines.",
            "Pompage localisé": "Utilisation d’un packer pour cibler une zone.",
            "Pistonnage": "Va-et-vient vertical pour mobiliser les particules.",
            "Jet haute pression": "Jets d’eau puissants pour décolmater les crépines.",
            "Air lift": "Injection d’air pour pomper et agiter l’eau.",
            "Traitement chimique": "Utilisation d’acide ou polyphosphate selon le colmatage."
        }
        st.write(f"🔧 {methode} : {dico[methode]}")
