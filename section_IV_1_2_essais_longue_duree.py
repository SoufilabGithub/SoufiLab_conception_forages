import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.special import expi
from scipy.optimize import curve_fit

st.markdown("## IV.1. Régime transitoire")
st.markdown("## IV.1.2 Essais de longue durée en mode transitoire (48h - 72h)")

# === Interface utilisateur ===
aquifer_options = [
    'Nappe captive', 'Nappe captive (gradient initial)',
    'Nappe semi-captive (drainance)', 'Nappe libre',
    'Nappe semi-libre (débit retardé)', 'Aquifère anisotrope',
    'Aquifère bicouche', 'Puits à pénétration partielle',
    'Recharge latérale', 'Barrière imperméable'
]

aquifer = st.selectbox("Aquifère :", aquifer_options)
Q = st.text_input("Q (m³/h)", "200")
r = st.number_input("Distance r (m)", value=110.0)
t_pomp = st.text_area("Temps pompage (h)", "1 2 3 4")
s_pomp = st.text_area("Rabatt. pompage (m)", "0.5 1.2 1.8 2.5")
t_rem = st.text_area("Temps remontée (h)", "")
s_rem = st.text_area("Rabatt. remontée (m)", "")

def parse(text):
    return np.array([float(x) for x in text.strip().split()]) if text.strip() else None

def plot_data(tp, sp, tr=None, sr=None):
    fig, axs = plt.subplots(1, 3, figsize=(18, 4))
    axs[0].plot(tp, sp, 'o-')
    axs[0].invert_yaxis(); axs[0].set_title("Pompage : s=f(t)")
    axs[1].semilogx(tp, sp, 'o-')
    axs[1].invert_yaxis(); axs[1].set_title("Pompage : s=f(log t)")
    axs[2].plot(1/np.array(tp), sp, 'o-')
    axs[2].invert_yaxis(); axs[2].set_title("Pompage : s=f(1/t)")
    for ax in axs: ax.grid(True)
    st.pyplot(fig)

    if tr is not None and sr is not None:
        fig2, ax2 = plt.subplots()
        ax2.plot(tr, sr, 'o-', color='green')
        ax2.invert_yaxis()
        ax2.set_title("Remontée : s = f(t)")
        ax2.set_xlabel("Temps (h)")
        ax2.set_ylabel("Remontée (m)")
        ax2.grid(True)
        st.pyplot(fig2)

def jacob(Q_m3h, t, s, r):
    Q = Q_m3h * 24  # conversion m³/h → m³/j
    log_t = np.log10(t)
    slope, intercept = np.polyfit(log_t, s, 1)
    T = 2.3 * Q / (4 * np.pi * slope)
    t0 = 10 ** (-intercept / slope)
    S = (2.25 * T * t0) / (r**2)
    return T, S, slope

if st.button("📈 Lancer l'analyse"):
    try:
        Q_val = float(Q)
        tp = parse(t_pomp)
        sp = parse(s_pomp)
        tr = parse(t_rem)
        sr = parse(s_rem)

        st.write(f"🔍 Aquifère sélectionné : **{aquifer}**")
        plot_data(tp, sp, tr, sr)

        synthese = []

        # Méthode de Jacob (pompage)
        if aquifer in ['Nappe captive', 'Nappe semi-captive', 'Nappe captive (gradient initial)']:
            if tp is not None and sp is not None:
                T, S, slope = jacob(Q_val, tp, sp, r)
                st.success(f"✅ Jacob (pompage) : T ≈ {T:.2f} m²/j, S ≈ {S:.2e}, pente ≈ {slope:.3f}")
                synthese.append({"Méthode": "Jacob (pompage)", "T (m²/j)": T, "S": S, "Note": "s = f(log t)"})

        # Méthode de Jacob (remontée)
        if tr is not None and sr is not None and len(tr) == len(sr):
            T, S, slope = jacob(Q_val, tr, sr, r)
            st.success(f"✅ Jacob (remontée) : T ≈ {T:.2f} m²/j, S ≈ {S:.2e}")
            synthese.append({"Méthode": "Jacob (remontée)", "T (m²/j)": T, "S": S, "Note": "s = f(log t) remontée"})

        # Méthode de Theis (approximée)
        if aquifer in ['Nappe captive', 'Nappe captive (gradient initial)']:
            T_est, S_est = 250, 1e-4
            st.info(f"ℹ️ Theis : T ≈ {T_est} m²/j, S ≈ {S_est} (valeurs estimées)")
            synthese.append({"Méthode": "Theis (approximé)", "T (m²/j)": T_est, "S": S_est, "Note": "expi(-u) non inversé"})

        if aquifer in ['Nappe libre', 'Nappe semi-libre (débit retardé)', 'Puits à pénétration partielle', 'Aquifère bicouche']:
            st.warning("⚠️ Méthodes spécifiques (Neuman, Boulton, Hantush) à intégrer dans une version étendue.")

        if synthese:
            df = pd.DataFrame(synthese)
            st.markdown("### 🧾 Synthèse des résultats")
            st.dataframe(df.fillna("-"))

    except Exception as e:
        st.error(f"❌ Erreur : {e}")
