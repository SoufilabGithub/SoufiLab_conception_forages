import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


st.markdown("## IV.1. Régime transitoire")
st.markdown("## IV.1.1 Essais par paliers ou de courte durée en mode transitoire")
st.markdown("### 🔎 Interprétation complète des essais par paliers")

# === Saisie des données ===
q_input = st.text_area("Débits Q (m³/h)", "10, 20, 30, 40, 50, 60, 70, 80, 90, 100")
s_input = st.text_area("Rabattements s (m)", "1, 2, 3, 4, 5, 6.1, 7.4, 8.9, 10.6, 12.5")
t_input = st.text_area("Temps t (min)", "60, 120, 180, 240, 300, 360, 420, 480, 540, 600")
H = st.number_input("Épaisseur H (m)", value=5.0)
nappe_type = st.radio("Type de nappe", ["libre", "captive"])
method_options = st.multiselect("Méthodes", ["Graphique Bi-Log", "Méthode de Rorabaugh", "Méthode de Gosselin"],
                                default=["Graphique Bi-Log", "Méthode de Rorabaugh", "Méthode de Gosselin"])

def rorabaugh(Q, s):
    def model(Q, A, B, n): return A * Q + B * Q**n
    popt, _ = curve_fit(model, Q, s, bounds=(0, [np.inf, np.inf, 5]))
    A, B, n = popt
    log_Q = np.log10(Q)
    s_Q_A = s / Q - A
    log_s_Q_A = np.log10(s_Q_A)
    return A, B, n, log_Q, log_s_Q_A

def gosselin(Q, s):
    def model(Q, B, n): return B * Q**n
    popt, _ = curve_fit(model, Q, s, bounds=(0, [np.inf, 5]))
    B, n = popt
    log_Q = np.log10(Q)
    log_s = np.log10(s)
    return B, n, log_Q, log_s

if st.button("Interpréter"):
    try:
        Q = np.array([float(x) for x in q_input.strip().split(',')])
        s = np.array([float(x) for x in s_input.strip().split(',')])
        t = np.array([float(x) for x in t_input.strip().split(',')])

        if not (len(Q) == len(s) == len(t)):
            st.error("❌ Q, s, t doivent avoir la même longueur.")
        else:
            s_sur_Q, Q_sur_s = s / Q, Q / s
            B, A = np.polyfit(Q, s, 2)[:2]
            s_model = A * Q + B * Q**2
            diff_s, pente_var = np.gradient(s_model), np.gradient(np.gradient(s_model))
            Qc = Q[np.argmax(pente_var)]
            s_opt = s[np.argmax(pente_var)]
            q_spec = np.mean(Q_sur_s)
            s_max = H / 3 if nappe_type == "libre" else 0.75 * H
            Qmax = s_max * q_spec
            eta = (A * Qc) / (A * Qc + B * Qc**2) * 100

            df = pd.DataFrame({"Q (m³/h)": Q, "s (m)": s, "t (min)": t,
                               "s/Q": s_sur_Q, "Q/s": Q_sur_s,
                               "Ls = AQ": A * Q, "Qs = BQ²": B * Q**2})
            st.dataframe(df)

            st.success(f"✅ Modèle classique : s = AQ + BQ²  →  A = {A:.4f}, B = {B:.4f}")
            st.info(f"📌 Qc = {Qc:.2f} m³/h ; s(Qc) = {s_opt:.2f} m ; η = {eta:.1f}%")
            st.info(f"📌 s_max = {s_max:.2f} m  →  Qmax ≈ {Qmax:.2f} m³/h")

            fig, axs = plt.subplots(3, 2, figsize=(14, 12))
            axs[0, 0].plot(Q, s, 'o-', label="s(Q)")
            axs[0, 0].plot(Q, s_model, '--', label="Modèle")
            axs[0, 0].axvline(Qc, color='red', linestyle=':', label="Qc")
            axs[0, 0].invert_yaxis(); axs[0, 0].legend(); axs[0, 0].set_title("s = f(Q)")

            axs[0, 1].plot(Q, s_sur_Q, 's-', color='orange')
            axs[0, 1].axvline(Qc, color='red', linestyle=':')
            axs[0, 1].invert_yaxis(); axs[0, 1].set_title("s/Q = f(Q)")

            axs[1, 0].loglog(Q, s, 'o-')
            axs[1, 0].axvline(Qc, color='red', linestyle=':')
            axs[1, 0].set_title("Graphique Bi-log")

            axs[1, 1].plot(t, s, 'd-', color='green')
            axs[1, 1].invert_yaxis()
            axs[1, 1].set_title("s = f(t)")

            if "Méthode de Rorabaugh" in method_options:
                A_r, B_r, n_r, log_Q_r, log_s_Q_A = rorabaugh(Q, s)
                axs[2, 0].plot(log_Q_r, log_s_Q_A, 'o-', label=f"(n-1)={n_r-1:.2f}")
                axs[2, 0].axvline(np.log10(Qc), color='red', linestyle=':', label="Qc")
                axs[2, 0].set_title("Rorabaugh : Log(s/Q - A) = f(Log Q)")
                axs[2, 0].legend()
                st.write(f"📘 Rorabaugh : A = {A_r:.4f}, B = {B_r:.4f}, n = {n_r:.2f}")

            if "Méthode de Gosselin" in method_options:
                B_g, n_g, log_Q_g, log_s_g = gosselin(Q, s)
                axs[2, 1].plot(log_Q_g, log_s_g, 'o-', label=f"n={n_g:.2f}")
                axs[2, 1].axvline(np.log10(Qc), color='red', linestyle=':', label="Qc")
                axs[2, 1].set_title("Gosselin : Log(s) = f(Log Q)")
                axs[2, 1].legend()
                st.write(f"📙 Gosselin : B = {B_g:.4f}, n = {n_g:.2f}")

            st.pyplot(fig)

            st.markdown("### 🔎 Analyse du type de puits")
            if all(np.diff(Q) > 0) and all(np.diff(s) > 0):
                if any(np.diff(s) < 0):
                    st.warning("❗ Anomalie : auto-développement")
                elif B < 0.001:
                    st.success("💧 Puits parfait")
                elif eta > 70:
                    st.success("🔎 Puits réel bien développé")
                elif eta < 50:
                    st.error("⚠️ Puits vieilli ou mal dimensionné")
                else:
                    st.info("🧪 Puits réel à rendement moyen")
            else:
                st.error("❓ Données incohérentes")
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
