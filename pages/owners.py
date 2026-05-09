import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/real_estate_clean.csv")

# Page title
st.title("📊 Owner Type Analysis")

# Show distribution of Owner_Type
st.subheader("Owner Type Distribution")
owner_counts = df["Owner_Type"].value_counts()

st.write(owner_counts)

# Plot
fig, ax = plt.subplots()
sns.countplot(data=df, x="Owner_Type", palette="Set2", ax=ax)
ax.set_title("Owner Type Distribution")
st.pyplot(fig)

# Price comparison
st.subheader("Average Price per SqFt by Owner Type")
avg_price = df.groupby("Owner_Type")["Price_per_SqFt"].mean().sort_values()
st.write(avg_price)

fig2, ax2 = plt.subplots()
avg_price.plot(kind="bar", color="skyblue", ax=ax2)
ax2.set_ylabel("Avg Price per SqFt")
ax2.set_title("Price Comparison by Owner Type")
st.pyplot(fig2)
