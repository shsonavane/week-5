import streamlit as st
import pandas as pd
from apputil import survival_demographics, visualize_demographic, family_groups, last_names, visualize_families, determine_age_division, visualize_age_division

# Load Titanic dataset
df = pd.read_csv("https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv")

# ---------------------------------------
# Titanic Visualization 1
# ---------------------------------------
st.write(
    """
    # Titanic Visualization 1
    """
)

st.write("Did women in first class have a higher survival rate than men in other classes?")

st.write("### Survival Demographics Table")
st.dataframe(survival_demographics())
# Generate and display the figure
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)


# ---------------------------------------
# Titanic Visualization 2
# ---------------------------------------
st.write(
    """
    # Titanic Visualization 2
    """
)

# Pose your family-related research question
st.write("Did larger families in higher classes pay significantly higher fares?")

# Show family group statistics
st.write("### Family Groups Table")
st.dataframe(family_groups())

# Show last name counts
st.write("### Last Name Counts")
st.write(last_names())

# Generate and display the figure
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------
# Titanic Visualization 3 (Bonus Question)
# ---------------------------------------
st.write(
    """
    # Titanic Visualization 3 (Bonus)
    """
)

# Pose your research question
st.write("Were older passengers within each class more or less likely to survive?")

# Show updated dataset (only first 15 rows for readability)
st.write("### Data with Age Division Column")
st.dataframe(determine_age_division().head(15))

# Generate and display the figure
fig3 = visualize_age_division()
st.plotly_chart(fig3, use_container_width=True)
