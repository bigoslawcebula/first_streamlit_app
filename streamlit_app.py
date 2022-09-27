# import - importuje biblioteki pythona
import streamlit
import pandas
import snowflake.connector


###Generalnie, streamlit.title, .header, .text wypisuje na ekran pewne rzeczy

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


#przy użyciu pandas, jesteśmy w stanie wczytać plik z URL (pandas.read_csv)
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Let's set the index to be "Fruit" column header (from the CSV file), instead of the default which appears to be row number of the table
#Bez tej linii, zamiast nbazw owocow wybieralibysmy ich numer
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include (the index value was already set to "Fruit")
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
#streamlit.text(fruityvice_response) <--displays response code 200 (replaced with the line below)
#streamlit.text(fruityvice_response.json) <--also incorrect, needs to be as below
#streamlit.text(fruityvice_response.json()) <--this line will display json data, but we want it to be more readable

# Line below takes the json version of the response and normalizes it (what ever it means)
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# the line below displays the previously normalized data
# wyglada na to, ze streamlit.dataframe poprostu wyswietli dane jakie ma (np w zmiennej) jako TABELA
streamlit.dataframe(fruityvice_normalized)



###URL to access it is: https://bigoslawcebula-first-streamlit-app-streamlit-app-xvr8gj.streamlitapp.com/
