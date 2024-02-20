import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()

streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_row)

streamlit.text("Add a New Fruit to the List")
# Campo para que el usuario escriba el nombre de la fruta
new_fruit_name = streamlit.text_input('What fruit would you like to add?', '')
# Botón para enviar la fruta
if streamlit.button('Add Fruit'):
    # Verificar que el nombre de la fruta no esté vacío
    if new_fruit_name:
        # Conexión a Snowflake
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_cur = my_cnx.cursor()
        # Instrucción SQL para insertar la nueva fruta
        try:
            my_cur.execute("INSERT INTO fruit_load_list (fruit_name) VALUES (%s)", (new_fruit_name,))
            streamlit.success(f"Added {new_fruit_name} to the list!")
        except Exception as e:
            streamlit.error(f"Error adding {new_fruit_name} to the list: {e}")
        finally:
            my_cur.close()
            my_cnx.close()
    else:
        streamlit.error("Please enter a fruit name.")
