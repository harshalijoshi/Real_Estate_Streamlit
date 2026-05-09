import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/real_estate_clean.csv")

# Page title
st.title("📊 Availability Status Analysis")

# Show distribution of Availability_Status
st.subheader("Availability Status Distribution")
availability_counts = df["Availability_Status"].value_counts()

st.write(availability_counts)

# Plot distribution
fig, ax = plt.subplots()
sns.countplot(data=df, x="Availability_Status", palette="Set3", ax=ax)
ax.set_title("Availability Status Distribution")
ax.set_ylabel("Count")
st.pyplot(fig)

# Price comparison
st.subheader("Average Price per SqFt by Availability Status")
avg_price = df.groupby("Availability_Status")["Price_per_SqFt"].mean().sort_values()
st.write(avg_price)

fig2, ax2 = plt.subplots()
avg_price.plot(kind="bar", color="lightgreen", ax=ax2)
ax2.set_ylabel("Avg Price per SqFt")
ax2.set_title("Price Comparison by Availability Status")
st.pyplot(fig2)
