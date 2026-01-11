# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits which you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on smoothie")
st.write("Name on smothie will be",name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Select 5 Ingrident',my_dataframe,max_selections=5)

if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
   # st.write(ingredients_string)

    time_to_insert=st.button('Submit order')

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
st_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
