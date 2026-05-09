import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/real_estate_clean.csv")

st.title("🚗 Parking Space Analysis")

# Distribution of Parking Space
st.subheader("Parking Space Availability")
parking_counts = df["Parking_Space"].value_counts()
st.write(parking_counts)

# Donut chart
fig, ax = plt.subplots()
ax.pie(parking_counts, labels=parking_counts.index, autopct="%1.1f%%", startangle=90)
centre_circle = plt.Circle((0,0),0.70,fc="white")
fig.gca().add_artist(centre_circle)
ax.set_title("Parking Space Distribution")
st.pyplot(fig)

# Price comparison
st.subheader("Average Price per SqFt by Parking Space")
avg_price = df.groupby("Parking_Space")["Price_per_SqFt"].mean()
st.write(avg_price)

fig2, ax2 = plt.subplots()
avg_price.plot(kind="bar", color=["skyblue", "orange"], ax=ax2)
ax2.set_ylabel("Avg Price per SqFt")
ax2.set_title("Price Comparison by Parking Space")
st.pyplot(fig2)
