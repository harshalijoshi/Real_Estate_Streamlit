import streamlit as st
import pandas as pd
import joblib

# Load dataset
df = pd.read_csv("data/real_estate_clean.csv")

# Load trained model
model = joblib.load("models/price_prediction_model.joblib")


# Define rule-based Good Investment function
def is_good_investment(price_per_sqft, amenities_score, transport, schools_nearby):
    if (price_per_sqft < 5000 and
        amenities_score == "High" and
        transport == "High" and
        schools_nearby == "Yes"):
        return 1
    else:
        return 0

# Streamlit UI
st.title("🏠 Real Estate Analytics & Prediction")
st.sidebar.title("Navigation")
option = st.sidebar.radio("Select Section", ["Home", "Prediction", "Analytics"])

# ---------------- HOME PAGE ----------------
if option == "Home":
    st.subheader("Welcome to the Real Estate Dashboard")
    st.write("""
    Use the sidebar to explore:
    - **Prediction**: Estimate property prices and check if it's a good investment.
    - **Analytics**: Explore city/locality trends, amenities impact, and feature importance.
    """)

# ---------------- PREDICTION PAGE ----------------
elif option == "Prediction":
    st.subheader("Property Price Prediction")

    # Inputs
    city = st.selectbox("City", df["City"].unique())

    # Locality dropdown filtered by selected City
    locality_options = df[df["City"] == city]["Locality"].unique()
    locality = st.selectbox("Locality", locality_options)

    bhk = st.number_input("BHK", min_value=1, max_value=10, step=1)
    size = st.number_input("Size (SqFt)", min_value=200, max_value=10000, step=50)
    transport = st.selectbox("Public Transport Accessibility", df["Public_Transport_Accessibility"].unique())
    parking = st.selectbox("Parking Space", df["Parking_Space"].unique())
    security = st.selectbox("Security", df["Security"].unique())
    facing = st.selectbox("Facing", df["Facing"].unique())
    owner_type = st.selectbox("Owner Type", df["Owner_Type"].unique())
    availability = st.selectbox("Availability Status", df["Availability_Status"].unique())

    # Amenities
    playground = st.checkbox("Playground")
    gym = st.checkbox("Gym")
    garden = st.checkbox("Garden")
    pool = st.checkbox("Pool")
    clubhouse = st.checkbox("Clubhouse")

    if st.button("Predict"):
        # Prepare input
        input_data = pd.DataFrame({
            "City":[city],
            "Locality":[locality],
            "Public_Transport_Accessibility":[transport],
            "Parking_Space":[parking],
            "Security":[security],
            "Facing":[facing],
            "Owner_Type":[owner_type],
            "Availability_Status":[availability],
            "BHK":[bhk],
            "Size_in_SqFt":[size],
            "Playground":[1 if playground else 0],
            "Gym":[1 if gym else 0],
            "Garden":[1 if garden else 0],
            "Pool":[1 if pool else 0],
            "Clubhouse":[1 if clubhouse else 0]
        })

        # Regression prediction
        predicted_price = model.predict(input_data)[0]

        # Classification (rule-based)
        amenities_score = "High" if (playground + gym + garden + pool + clubhouse) >= 3 else "Low"
        investment_flag = is_good_investment(predicted_price, amenities_score, transport, "Yes")

        # Future price (simple appreciation assumption)
        future_price = predicted_price * 1.25

        # Show results
        st.success(f"Estimated Price per SqFt: {predicted_price:.2f}")
        st.info(f"Estimated Price after 5 Years: {future_price:.2f}")

        if investment_flag == 1:
            st.success("✅ This property is a Good Investment!")
        else:
            st.warning("⚠️ This property may not be a good investment.")

# ---------------- ANALYTICS PAGE ----------------
elif option == "Analytics":
    st.subheader("📊 Explore Analytics")

    # Dropdown to select a City
    selected_city = st.selectbox("Select City for Analysis", df["City"].unique())
    city_df = df[df["City"] == selected_city]

    st.write(f"### Insights for {selected_city}")

    # Average price per SqFt
    avg_price = city_df["Price_per_SqFt"].mean()
    st.metric(label="Average Price per SqFt", value=f"{avg_price:.2f}")

    # Distribution of property sizes
    st.write("#### Property Size Distribution")
    st.bar_chart(city_df["Size_in_SqFt"])

    # Amenity availability counts
    st.write("#### Amenity Availability")
    amenities = ["Playground", "Gym", "Garden", "Pool", "Clubhouse"]
    amenity_counts = city_df[amenities].sum()
    st.bar_chart(amenity_counts)

    # Price impact of amenities
    st.write("#### Average Price per SqFt with vs. without Amenities")
    for amenity in amenities:
        avg_price_by_amenity = city_df.groupby(amenity)["Price_per_SqFt"].mean()
        st.write(f"{amenity}:")
        st.bar_chart(avg_price_by_amenity)

    # Global overview: Top 5 expensive cities
    st.write("### Top 5 Most Expensive Cities (Overall)")
    city_avg = df.groupby("City")["Price_per_SqFt"].mean().sort_values(ascending=False).head(5)
    st.bar_chart(city_avg)
