# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

import streamlit as st

name_on_order = st.text_input("Name of smoothie:")
st.write("The name on your smoothie will be:", name_on_order)
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options")
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'choose upto 5 ingredients:'
    ,my_dataframe.select(col("FRUIT_NAME")).to_pandas()["FRUIT_NAME"]
,max)
if ingredients_list:
     st.write(ingredients_list)
     st.text(ingredients_list)
     if ingredients_list:
          ingredients_string = ", ".join(ingredients_list)

          st.write(ingredients_string)

     my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
"""


     st.write(my_insert_stmt)

     time_to_insert=st.button('submit order')
     if time_to_insert:
          session.sql(my_insert_stmt).collect()
          st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")
