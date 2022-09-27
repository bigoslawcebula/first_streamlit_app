### To jest GitHUB, czyli miejsce gdzie przechowywany jest kod. Natomiast nie jest on tutaj uruchomiony. Jest uruchomiany w streamlit, 
### czyli platformie uruchomieniowej kodu napisanego chyba tylko w python, ma tez swoją własną biblioteke


# import - importuje biblioteki pythona
import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

###Generalnie, streamlit.title, .header, .text wypisuje na ekran pewne rzeczy

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


#przy użyciu biblioteki pandas, jesteśmy w stanie wczytać plik z URL (pandas.read_csv) --> wiecej o pandas: https://analityk.edu.pl/python-pandas/
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Let's set the index to be "Fruit" column header (from the CSV file), instead of the default which appears to be row number of the table
#Bez tej linii, zamiast nbazw owocow wybieralibysmy ich numer
my_fruit_list = my_fruit_list.set_index('Fruit')

### Let's put a pick list here so they can pick the fruit they want to include (the index value was already set to "Fruit")
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries']) ###ten index wczesniej zamieniono na nazwe owocu
fruits_to_show = my_fruit_list.loc[fruits_selected] ###nowa zmienna, 

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


### WERSJA 1


#streamlit.header("Fruityvice Fruit Advice! -- ver 1")
###pobieramy dane poprzez API i zapisujemy je w zmiennej fruityvice_response, żeby potem z tej odpowiedzi serwera móc wyłuskiwać różne elementy
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
###streamlit.text(fruityvice_response) <--displays response code 200 (replaced with the line below)
###streamlit.text(fruityvice_response.json) <--also incorrect, needs to be as below
###streamlit.text(fruityvice_response.json()) <--this line will display json data, but we want it to be more readable

### Line below takes the json version of the response and normalizes it (what ever it means --> https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html)
### Normalizacja polega na zamiania semi-structured data (jak JSON) na dane znormalizowane, czyli w formie tabeli
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
### the line below displays the previously normalized data
### wyglada na to, ze streamlit.dataframe poprostu wyswietli dane jakie ma (np w zmiennej) jako TABELA
#streamlit.dataframe(fruityvice_normalized)

### WERSJA 2
#streamlit.header("Fruityvice Fruit Advice! -- ver 2")
#fruit_choice = streamlit.text_input("What fruit would you like information about?") ###pobieramy od użytkownika wartość
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice) ###wykonujemy API call z tą wartością
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) ###normalizujemy wynik (czyli semi-structured data zamieniamy na dane ustrukturyzowane)
#streamlit.dataframe(fruityvice_normalized) ###wyświetlamy wynik w formie tabeli


### WERSJA 3
#streamlit.header("Fruityvice Fruit Advice!")
#try:
#  fruit_choice = streamlit.text_input('What fruit would you like information about?') ###pobieramy od użytkownika wartość
#  if not fruit_choice:
#    streamlit.error("Please select a fruit to get information.")
#  else:  
#    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice) ###wykonujemy API call z tą wartością
#    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) ###normalizujemy wynik (cokolwiek to oznacza)
#    streamlit.dataframe(fruityvice_normalized) ###wyświetlamy wyniok w formie tabeli

#except URLError as e:
#  streamlit.error()

  
 ### WERSJA 4 (z funkcją)
def get_fruityvice_data(this_fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice) ###wykonujemy API call z tą wartością
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) ###normalizujemy wynik (cokolwiek to oznacza)
    return fruityvice_normalized #nie wiem co to robi, ale to pewnie jakies zakonczenie funkcji
streamlit.header("Fruityvice Fruit Advice!")
try:
  this_fruit_choice = streamlit.text_input('What fruit would you like information about?') ###pobieramy od użytkownika wartość
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:  
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function) ###wyświetlamy wyniok w formie tabeli

except URLError as e:
  streamlit.error()
  
 
 

####### TEMPORARY blocking the code from inserting rows int the table
streamlit.stop()
#######

# ADDING SNOWFLAKE
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) ###łączy się z użyciem sekretów, które skonfigurowalismy w streamlit
my_cur = my_cnx.cursor() ###to nie mam pojęcia co robi
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") ##to juz wyglada na faktyczny statement, ale chyba zdefiniowanie zapytania a nie uruchomienie (moge sie mylic)
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

# Inne zapytanie do Snowflake
# kolejny raz prosimy Snowflake o dane
my_cur.execute("select * from fruit_load_list")
# poniższe chyba dopiero faktycznie pozyskuje dane i zapisuje w zmiennej, używająć powyżej zdefiniowanego query) --> https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
my_data_row = my_cur.fetchone()
# wypisujemy dane:
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)

# A teraz wypiszemy to samo, ale inaczej
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# jednach chcemy wszystkie wiersze nie tylko jeden, wiec użyjemy fetchall zamiast fetchone
# w tym celu musimy na nowo pobrac dane i zapisać w zmienenj:
my_data_row = my_cur.fetchall()
# a teraz jeszcze raz wypiszemy sobie te dane:
streamlit.header("The fruit load list contains: {FETCHALL}")
streamlit.dataframe(my_data_row)


# allowing a user to add a fruit to the list
add_my_fruit = streamlit.text_input("What fruit would you like to add?", help="Provide the fruit you would like to add and press enter")
streamlit.write('Thanks for adding ', add_my_fruit)

#adding values into snowflake
my_cur.execute("insert into fruit_load_list values ('from streamlit')")

###URL to access it is: https://bigoslawcebula-first-streamlit-app-streamlit-app-xvr8gj.streamlitapp.com/
