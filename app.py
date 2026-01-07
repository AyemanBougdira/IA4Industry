import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Stabilité thermique du four avec combustibles alternatifs")

# --- Paramètres du four ---
st.header("Paramètres du four")
T_initial = st.number_input("Température initiale du four (°C)", value=25.0)
capacite_thermique = st.number_input(
    "Capacité thermique du four (kJ/°C)", value=5000.0)
temps_simulation = st.number_input("Durée simulation (heures)", value=5.0)

# --- Combustibles alternatifs ---
st.header("Combustibles alternatifs")

comb1 = st.text_input("Nom combustible 1", "Biomasse")
masse1 = st.number_input(f"Masse {comb1} (kg/h)", value=100.0)

comb2 = st.text_input("Nom combustible 2", "Coke")
masse2 = st.number_input(f"Masse {comb2} (kg/h)", value=50.0)

# --- Pouvoir calorifique inconnu ---
st.header("Estimation du pouvoir calorifique (PCI)")
st.write("Le PCI est inconnu : on simule un intervalle ou on estime avec IA")

# Option 1: Intervalle de PCI (simulation paramétrique)
pci_min = st.number_input("PCI minimum estimé (kJ/kg)", value=15000.0)
pci_max = st.number_input("PCI maximum estimé (kJ/kg)", value=30000.0)

# --- Simulation ---
temps = np.linspace(0, temps_simulation, 100)

# Calcul pour PCI min
energie_min = (pci_min*masse1 + pci_min*masse2)  # simplification
delta_T_min = energie_min / capacite_thermique
temperature_min = T_initial + delta_T_min * temps

# Calcul pour PCI max
energie_max = (pci_max*masse1 + pci_max*masse2)
delta_T_max = energie_max / capacite_thermique
temperature_max = T_initial + delta_T_max * temps

# --- Affichage des résultats ---
st.subheader("Simulation paramétrique : zone de sécurité thermique")
st.write(f"Température finale minimale : {temperature_min[-1]:.2f} °C")
st.write(f"Température finale maximale : {temperature_max[-1]:.2f} °C")

# --- Graphique ---
fig, ax = plt.subplots()
ax.plot(temps, temperature_min, label="PCI min")
ax.plot(temps, temperature_max, label="PCI max")
ax.fill_between(temps, temperature_min, temperature_max,
                color='orange', alpha=0.3, label="Zone probable")
ax.set_xlabel("Temps (h)")
ax.set_ylabel("Température (°C)")
ax.set_title("Stabilité thermique avec PCI inconnu")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# --- Option IA simplifiée ---
st.header("Estimation PCI avec IA (simulation)")
use_ia = st.checkbox("Activer estimation IA du PCI")

if use_ia:
    st.write(
        "💡 Ici, une IA pourrait prédire le PCI à partir de caractéristiques du combustible.")
    st.write("Exemple : pour la biomasse humide, le PCI estimé = 20000 kJ/kg")
    pci_estime = 20000
    energie_estime = (pci_estime*masse1 + pci_estime*masse2)
    delta_T_estime = energie_estime / capacite_thermique
    temperature_estime = T_initial + delta_T_estime * temps

    st.write(
        f"Température finale estimée par IA : {temperature_estime[-1]:.2f} °C")

    fig2, ax2 = plt.subplots()
    ax2.plot(temps, temperature_estime, label="PCI estimé IA", color='green')
    ax2.set_xlabel("Temps (h)")
    ax2.set_ylabel("Température (°C)")
    ax2.set_title("Estimation IA de la stabilité thermique")
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)
