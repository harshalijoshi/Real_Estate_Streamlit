import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/real_estate_clean.csv")

st.title("🚉 Transport & Connectivity Analysis")

# List of transport-related features (adjust to match your dataset columns)
transport_features = ["Nearby_Hospitals", "Nearby_Schools"]

# Donut chart for distribution
st.subheader("Connectivity Distribution")
for feature in transport_features:
    st.write(f"### {feature} Availability")
    counts = df[feature].value_counts()

    fig, ax = plt.subplots()
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
    centre_circle = plt.Circle((0,0),0.70,fc="white")
    fig.gca().add_artist(centre_circle)
    ax.set_title(f"{feature} Distribution (Yes/No)")
    st.pyplot(fig)

# Boxplot for price comparison
st.subheader("Price per SqFt by Connectivity")
for feature in transport_features:
    st.write(f"### {feature} Impact on Price")
    fig2, ax2 = plt.subplots(figsize=(6,4))
    sns.boxplot(data=df, x=feature, y="Price_per_SqFt", palette="Set2", ax=ax2)
    ax2.set_title(f"Price per SqFt vs {feature}")
    st.pyplot(fig2)
