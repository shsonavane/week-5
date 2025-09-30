import plotly.express as px
import pandas as pd

# update/add code below ...
# Exercise-1---------------------------------------
def survival_demographics():
    url = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"
    df = pd.read_csv(url)

    # Create Age Group categories
    bins = [0, 12, 19, 59, float("inf")]
    labels = ["Child", "Teen", "Adult", "Senior"]
    df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)

    # Group by Pclass, Sex, AgeGroup
    grouped = (
        df.groupby(["Pclass", "Sex", "AgeGroup"])
        .agg(
            n_passengers=("Survived", "size"),
            n_survivors=("Survived", "sum")
        )
        .reset_index()
    )

    # Calculate survival rate
    grouped["survival_rate"] = grouped["n_survivors"] / grouped["n_passengers"]

    # Ensure all class/sex/age group combos appear
    all_combinations = pd.MultiIndex.from_product(
        [sorted(df["Pclass"].dropna().unique()),
         sorted(df["Sex"].dropna().unique()),
         labels],
        names=["Pclass", "Sex", "AgeGroup"]
    )
    grouped = grouped.set_index(["Pclass", "Sex", "AgeGroup"]).reindex(all_combinations, fill_value=0).reset_index()

    # Sort results
    grouped = grouped.sort_values(["Pclass", "Sex", "AgeGroup"]).reset_index(drop=True)
    return grouped


def visualize_demographic():
    grouped = survival_demographics()

    fig = px.bar(
        grouped,
        x="AgeGroup",
        y="survival_rate",
        color="Sex",
        barmode="group",
        facet_col="Pclass",
        category_orders={"AgeGroup": ["Child", "Teen", "Adult", "Senior"]},
        title="Titanic Survival Rates by Class, Sex, and Age Group"
    )
    fig.update_layout(yaxis=dict(title="Survival Rate"), xaxis=dict(title="Age Group"))
    return fig


# Exercise-2---------------------------------------
# 1. Family groups analysis
def family_groups():
    url = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"
    df = pd.read_csv(url)

    # Create family size column
    df["family_size"] = df["SibSp"] + df["Parch"] + 1

    # Group by family size and passenger class
    grouped = (
        df.groupby(["Pclass", "family_size"])
        .agg(
            n_passengers=("PassengerId", "size"),
            avg_fare=("Fare", "mean"),
            min_fare=("Fare", "min"),
            max_fare=("Fare", "max")
        )
        .reset_index()
    )

    # Sort by class then family size
    grouped = grouped.sort_values(["Pclass", "family_size"]).reset_index(drop=True)
    return grouped


# 2. Extract last names and count
def last_names():
    url = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"
    df = pd.read_csv(url)

    # Extract last names (everything before the comma in Name column)
    df["LastName"] = df["Name"].str.split(",").str[0].str.strip()

    # Count occurrences of each last name
    last_name_counts = df["LastName"].value_counts()
    return last_name_counts


# 3. Visualization for family groups
def visualize_families():
    grouped = family_groups()

    # Example question:
    # "Did larger families in higher classes pay significantly higher fares?"
    fig = px.bar(
        grouped,
        x="family_size",
        y="avg_fare",
        color="Pclass",
        barmode="group",
        title="Average Fare by Family Size and Passenger Class",
        labels={"avg_fare": "Average Fare", "family_size": "Family Size", "Pclass": "Passenger Class"},
    )

    fig.update_layout(
        xaxis=dict(title="Family Size"),
        yaxis=dict(title="Average Ticket Fare"),
        legend_title="Passenger Class"
    )
    return fig


#Bonus Question-------------------
    #  Bonus Question: Determine age division within each class
def determine_age_division():
    url = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"
    df = pd.read_csv(url)

    # Compute median age per passenger class
    class_median = df.groupby("Pclass")["Age"].transform("median")

    # New Boolean column: older_passenger
    df["older_passenger"] = df["Age"] > class_median

    return df


#  Bonus Visualization
def visualize_age_division():
    df = determine_age_division()

    # Example question:
    # "Were older passengers within each class more or less likely to survive?"
    fig = px.histogram(
        df,
        x="Pclass",
        color="older_passenger",
        barmode="group",
        facet_col="Sex",
        y="Survived",
        histfunc="avg",
        title="Survival Rate by Passenger Class and Age Division",
        labels={"Survived": "Survival Rate", "older_passenger": "Older than Median Age"}
    )

    fig.update_layout(
        xaxis_title="Passenger Class",
        yaxis_title="Survival Rate",
        legend_title="Older Passenger"
    )
    return fig
