# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits for your smoothie.
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
#option = st.selectbox('Which fruit would you like?',
#                      ('Apple','Banana','Peach','Strawberry'))
#st.write('You selected ' , option)

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie will be : ', name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)
if ingredients_list:
#    st.write(ingredients_list)
#    st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        sf_response = requests.get("https://my.smoothiefroot.com/api/fruit/mango")
        #st.text(sf_response)  # returns HTTP response code like 200 or 404
        sf_df = st.dataframe(data=sf_response.json(), use_container_width=True)
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
#new section to display nutrition information from smoothiefroot.com using API calls



