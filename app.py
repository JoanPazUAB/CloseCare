import streamlit
import pandas
# import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list) només mostra dataset estàtic
my_fruit_list = my_fruit_list.set_index('Fruit') #mostra el nom de la fruita com a índex en comptes de 1,2,3,4...

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
frui_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(frui_to_show)

#Creaete Section to display fruityvice api response
def get_fruityvice_data(this_fruit_choice):
   #streamlit.text(fruityvice_response.json()) #s'escriuen per pantalla les dades
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice) #s'agafen dades de watermelon
    # Normalitza el json: fa que per cada atribut numèric no creï una fila al fer el dataframe a streamlit
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # Crea a dataframe/taula el resultat normalitzat
    return fruityvice_normalized
