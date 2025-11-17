import streamlit as st
import pandas as pd

# -------------------------------------------
# LOAD EXCEL FILES
# -------------------------------------------
bp_file = "High low BP data.xlsx"
diabetes_file = "Diabetic data.xlsx"

bp_df = pd.read_excel(bp_file)
diabetes_df = pd.read_excel(diabetes_file)

# Convert text columns to lowercase for matching
bp_df["Gender"] = bp_df["Gender"].astype(str).str.lower()
bp_df["Blood_Pressure_Level"] = bp_df["Blood_Pressure_Level"].astype(str).str.lower()
diabetes_df["Gender"] = diabetes_df["Gender"].astype(str).str.lower()
diabetes_df["Diabetes_Type"] = diabetes_df["Diabetes_Type"].astype(str).str.lower()

# -------------------------------------------
# FLOAT RANGE FUNCTION FOR A1C OPTIONS
# -------------------------------------------
def frange(start, stop, step):
    while start <= stop:
        yield round(start, 1)
        start += step

# -------------------------------------------
# STREAMLIT UI
# -------------------------------------------
st.title("🩺 Health Recommendation System")
st.write("Enter your details to get the correct diet, drinks, sleep, and exercise plan.")

# User selects condition
condition = st.selectbox("Select Health Condition", ["Blood Pressure", "Diabetes"])

# -------------------------------------------
# BLOOD PRESSURE SECTION
# -------------------------------------------
if condition == "Blood Pressure":
    age = st.selectbox("Select Age", sorted(bp_df["Age"].unique().tolist()))
    gender = st.selectbox("Select Gender", sorted(bp_df["Gender"].unique().tolist()))
    bp_level = st.selectbox("Select Blood Pressure Level", sorted(bp_df["Blood_Pressure_Level"].unique().tolist()))

    def get_plan(age, gender, bp):
        result = bp_df[
            (bp_df["Age"] == age) &
            (bp_df["Gender"] == gender) &
            (bp_df["Blood_Pressure_Level"] == bp)
        ]
        if result.empty:
            return None
        return result.iloc[0]

    if st.button("Get Recommendation"):
        row = get_plan(age, gender, bp_level)
        if row is None:
            st.error("No matching record found in the BP dataset.")
        else:
            st.success("🍏 Your Health Recommendation Plan for BP")
            st.write("### ✔ Foods To Eat"); st.info(row["Foods_To_Eat"])
            st.write("### ❌ Foods To Avoid"); st.warning(row["Foods_To_Avoid"])
            st.write("### 🥤 Recommended Drinks"); st.info(row["Recommended_Drinks"])
            st.write("### 🧂 Daily Salt Intake (g)"); st.info(row["Daily_Salt_Intake(g)"])
            st.write("### 😴 Sleep Hours"); st.info(row["Sleep_Hours"])
            st.write("### 🏃 Exercise Type"); st.info(row["Exercise_Type"])
            st.write("### ⏱ Exercise Duration (min)"); st.info(row["Exercise_Duration(min)"])

# -------------------------------------------
# DIABETES SECTION
# -------------------------------------------
elif condition == "Diabetes":
    age = st.selectbox("Select Age", sorted(diabetes_df["Age"].unique().tolist()))
    gender = st.selectbox("Select Gender", sorted(diabetes_df["Gender"].unique().tolist()))
    diabetes_type = st.selectbox("Select Diabetes Type", sorted(diabetes_df["Diabetes_Type"].unique().tolist()))

    # Create A1C range from 6.0 → 9.9
    a1c_values = [x for x in frange(6.0, 9.9, 0.1)]
    a1c_level = st.selectbox("Enter A1C Level (%)", a1c_values)

    def get_plan_diabetes(age, gender, diabetes_type, a1c_level):
        result = diabetes_df[
            (diabetes_df["Age"] == age) &
            (diabetes_df["Gender"] == gender) &
            (diabetes_df["Diabetes_Type"] == diabetes_type) &
            (diabetes_df["A1C_Level (%)"] == a1c_level)
        ]
        if result.empty:
            return None
        return result.iloc[0]

    if st.button("Get Diabetes Recommendation"):
        row = get_plan_diabetes(age, gender, diabetes_type.lower(), a1c_level)
        if row is None:
            st.error("No matching record found in the Diabetes dataset.")
        else:
            st.success("🍏 Your Health Recommendation Plan for Diabetes")
            st.write("### ✔ Foods To Eat"); st.info(row["Foods_To_Eat"])
            st.write("### ❌ Foods To Avoid"); st.warning(row["Foods_To_Avoid"])
            st.write("### 🥤 Recommended Drinks"); st.info(row["Recommended_Drinks"])
            st.write("### 🍞 Daily Carb Target (g)"); st.info(row["Daily_carbohydrates_Target (g)"])
            st.write("### 😴 Sleep Hours"); st.info(row["Sleep_Hours"])
            st.write("### 🏃 Exercise Type"); st.info(row["Exercise_Type"])
            st.write("### ⏱ Exercise Duration (min)"); st.info(row["Exercise_Duration (min)"])

# Footer
st.markdown("##### 2025 Ritik Kumar | 🍏 Your Health Recommendation Plan")
