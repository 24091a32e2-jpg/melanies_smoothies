# Import packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit table with SEARCH_ON column
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"), col("SEARCH_ON")
)

# Convert Snowpark dataframe to Pandas
pd_df = my_dataframe.to_pandas()

# Optional: show dataframe for debugging
# st.dataframe(pd_df)

# Multiselect using FRUIT_NAME column
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + " "

        # Get SEARCH_ON value from dataframe
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"
        ].iloc[0]

        st.write("The search value for", fruit_chosen, "is", search_on, ".")

        # Section title
        st.subheader(fruit_chosen + " Nutrition Information")

        # API call using SEARCH_ON value
        response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        data = response.json()

        # Handle fruits not found in API
        if "error" in data:
            st.write(data)
        else:
            st.dataframe(data, use_container_width=True)

    # Insert order section
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")
