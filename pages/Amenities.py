import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/real_estate_clean.csv")

st.title("🏡 Amenities Analysis")

# List of amenities to analyze
amenities = ["Playground", "Gym", "Garden", "Pool", "Clubhouse"]

# Convert 0/1 to Yes/No for display
df_yesno = df.copy()
for amenity in amenities:
    df_yesno[amenity] = df_yesno[amenity].map({0: "No", 1: "Yes"})

# Show counts for each amenity
st.subheader("Amenity Availability Counts")
amenity_counts = {amenity: df_yesno[amenity].value_counts().to_dict() for amenity in amenities}
st.write(amenity_counts)

# Plot counts for each amenity
for amenity in amenities:
    st.write(f"### {amenity} Distribution")
    fig, ax = plt.subplots()
    df_yesno[amenity].value_counts().plot(kind="bar", color=["skyblue", "orange"], ax=ax)
    ax.set_ylabel("Count")
    ax.set_title(f"{amenity} Availability (Yes/No)")
    st.pyplot(fig)

# Average price per SqFt by amenity (with Yes/No labels)
st.subheader("Average Price per SqFt by Amenity")
for amenity in amenities:
    st.write(f"### {amenity} Price Comparison")
    avg_price = df_yesno.groupby(amenity)["Price_per_SqFt"].mean()
    st.write(avg_price)

    fig2, ax2 = plt.subplots()
    avg_price.plot(kind="bar", color=["lightgreen", "salmon"], ax=ax2)
    ax2.set_ylabel("Avg Price per SqFt")
    ax2.set_title(f"Price per SqFt by {amenity} (Yes/No)")
    st.pyplot(fig2)
