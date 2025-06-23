import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.special as sc

st.markdown("## IV.2 Régime permanent : Essais de nappe en mode permanent")

# === Fonctions fondamentales ===
def calc_transmissivite(K, e):
    return K * e

def calc_permeabilite(T, e):
    return T / e

def calc_rayon_influence(H, s):
    return H * np.exp(2 * np.pi * s / H)

def calc_vitesse(Q, S, n):
    return Q / (S * n)

# === Méthodes ===
def thiem(Q, T, r, R):
    return (Q / (2 * np.pi * T)) * np.log(R / r)

def thiem_dupuit(Q, T, r, R, h0):
    s = thiem(Q, T, r, R)
    return h0 - s, s

def de_glee(Q, T, r, L):
    u = r / L
    return (Q / (4 * np.pi * T)) * sc.expn(0, u)

def hantush_drainance(Q, T, r, L):
    u = r / L
    return (Q / (4 * np.pi * T)) * sc.expn(0, u)

def gradient_initial(Q, T, r, R, i):
    return thiem(Q, T, r, R) + i * r

def huisman(Q, T, r, R, H, h):
    return thiem(Q, T, r, R) * (H / h)

def dietz(Q, T, r, a):
    return (Q / (4 * np.pi * T)) * np.log((a + np.sqrt(a**2 + r**2)) / r)

# === Contexte
contexts = {
    'Nappe libre sans réalimentation': ['Q', 'T', 'r1', 'R', 'h0'],
    'Nappe captive sans réalimentation': ['Q', 'T', 'r1', 'R'],
    'Nappe semi-captive (drainance)': ['Q', 'T', 'r1', 'L'],
    'Nappe libre réalimentée': ['Q', 'T', 'r1', 'L'],
    'Nappe libre à substratum incliné': ['Q', 'T', 'r1', 'L'],
    'Nappe captive avec gradient initial': ['Q', 'T', 'r1', 'R', 'i'],
    'Aquifère à frontière rectiligne': ['Q', 'T', 'r1', 'a'],
    'Aquifère à pénétration partielle': ['Q', 'T', 'r1', 'R', 'H', 'h'],
    'Aquifère bicouche': ['Q', 'T', 'r1', 'L'],
    'Aquifère incliné à épaisseur constante': ['Q', 'T', 'r1', 'R', 'i'],
    'Nappe semi-libre': ['Q', 'T', 'r1', 'r2', 'h1', 'h2', 'e']
}

contexte = st.selectbox("Contexte", list(contexts.keys()))
inputs = {}
for param in contexts[contexte]:
    inputs[param] = st.number_input(param, value=1.0, step=0.1)

K = st.number_input("K (m/s)", value=0.002)
e = st.number_input("Épaisseur e (m)", value=30.0)
n = st.number_input("Porosité n", value=0.25)
H = st.number_input("Hauteur nappe H (m)", value=20.0)

if st.button("▶️ Calculer"):
    try:
        s = 0
        if contexte == 'Nappe libre sans réalimentation':
            _, s = thiem_dupuit(inputs['Q'], inputs['T'], inputs['r1'], inputs['R'], inputs['h0'])
            methode = "Thiem-Dupuit"
        elif contexte == 'Nappe captive sans réalimentation':
            s = thiem(inputs['Q'], inputs['T'], inputs['r1'], inputs['R'])
            methode = "Thiem"
        elif contexte == 'Nappe semi-captive (drainance)':
            s = (de_glee(inputs['Q'], inputs['T'], inputs['r1'], inputs['L']) +
                 hantush_drainance(inputs['Q'], inputs['T'], inputs['r1'], inputs['L'])) / 2
            methode = "De Glee & Hantush"
        elif contexte == 'Nappe libre réalimentée':
            s = hantush_drainance(inputs['Q'], inputs['T'], inputs['r1'], inputs['L'])
            methode = "Hantush"
        elif contexte == 'Nappe libre à substratum incliné':
            s = hantush_drainance(inputs['Q'], inputs['T'], inputs['r1'], inputs['L'])
            methode = "Hantush inclinée"
        elif contexte == 'Nappe captive avec gradient initial':
            s = gradient_initial(inputs['Q'], inputs['T'], inputs['r1'], inputs['R'], inputs['i'])
            methode = "Hantush + gradient"
        elif contexte == 'Aquifère à frontière rectiligne':
            s = dietz(inputs['Q'], inputs['T'], inputs['r1'], inputs['a'])
            methode = "Dietz"
        elif contexte == 'Aquifère à pénétration partielle':
            s = huisman(inputs['Q'], inputs['T'], inputs['r1'], inputs['R'], inputs['H'], inputs['h'])
            methode = "Huisman"
        elif contexte == 'Aquifère bicouche':
            s = de_glee(inputs['Q'], inputs['T'], inputs['r1'], inputs['L'])
            methode = "De Glee (bicouche)"
        elif contexte == 'Aquifère incliné à épaisseur constante':
            s = gradient_initial(inputs['Q'], inputs['T'], inputs['r1'], inputs['R'], inputs['i'])
            methode = "Hantush incliné"
        elif contexte == 'Nappe semi-libre':
            delta_h = inputs['h1'] - inputs['h2']
            ln_ratio = np.log(inputs['r2'] / inputs['r1'])
            K_est = (delta_h * inputs['e'] * np.pi) / (ln_ratio * inputs['Q'])
            s = delta_h
            methode = "Estimation semi-libre"
            st.info(f"Estimation K = {K_est:.2e} m/s")

        Tcalc = calc_transmissivite(K, e)
        vcalc = calc_vitesse(inputs['Q'], e, n)
        Rcalc = calc_rayon_influence(H, s)

        st.success(f"Méthode : {methode}")
        st.write(f"🔹 Rabattement : {s:.2f} m")
        st.write(f"🔹 Transmissivité T : {Tcalc:.2f} m²/j")
        st.write(f"🔹 Vitesse d’écoulement v : {vcalc:.2e} m/s")
        st.write(f"🔹 Rayon d’influence R : {Rcalc:.2f} m")

        if 'R' in inputs and inputs['R'] > 0:
            r_vals = np.linspace(inputs['r1'], inputs['R'], 100)
            s_vals = (inputs['Q'] / (2 * np.pi * Tcalc)) * np.log(inputs['R'] / r_vals)
            plt.plot(r_vals, s_vals)
            plt.title("Cône de rabattement")
            plt.xlabel("r (m)")
            plt.ylabel("s (m)")
            plt.grid(True)
            st.pyplot(plt.gcf())
    except Exception as e:
        st.error(f"Erreur de calcul : {e}")
