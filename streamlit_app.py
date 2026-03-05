# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input name
name_on_order = st.text_input("Name of smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options
my_dataframe = session.table("smoothies.public.fruit_options")

st.dataframe(data=my_dataframe, use_container_width=True)

# Convert Snowpark column to list
fruit_options = my_dataframe.select(col("FRUIT_NAME")).to_pandas()["FRUIT_NAME"].tolist()

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

if ingredients_list:
    st.write(ingredients_list)

    ingredients_string = ", ".join(ingredients_list)
    st.write(ingredients_string)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")

import streamlit as st
import requests

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
fruit_data = smoothiefroot_response.json()

flat_data = {
    'family': fruit_data['family'],
    'genus': fruit_data['genus'],
    'id': fruit_data['id'],
    'name': fruit_data['name'],
    'carbs': fruit_data['nutrition']['carbs'],
    'fat': fruit_data['nutrition']['fat'],
    'protein': fruit_data['nutrition']['protein'],
    'sugar': fruit_data['nutrition']['sugar'],
    'order': fruit_data['order']
}

st.dataframe(data=[flat_data], use_container_width=True)
