import streamlit as st
import pandas as pd
import requests
from streamlit_js_eval import streamlit_js_eval


if 'score' not in st.session_state:
    st.session_state['score'] = 0
if 'guesses' not in st.session_state:
    st.session_state['guesses'] = 0
if 'rerun' not in st.session_state:
    st.session_state['rerun'] = True
if 'guess_df' not in st.session_state:
    st.session_state['guess_df'] = pd.DataFrame([], columns=['price', 'guess', 'card'])

if st.session_state['rerun']:
    st.session_state['rerun'] = False
    query = 'https://api.scryfall.com/cards/random?q=set%3A7ed%20is%3Afoil'
    query_out = requests.get(query)
    content = query_out.json()
    st.session_state['content'] = content
else:
    content = st.session_state['content']

image_uri = content['image_uris']['border_crop']
price_raw = content['prices']['usd_foil']
card_name = content['name']
try:
    price = round(float(price_raw),0)
except:
    st.session_state['rerun'] = True
    st.rerun()


def run_guess(price, guess, card_name):
    score = abs(guess-price)
    new_df = pd.concat([st.session_state['guess_df'],pd.DataFrame([{
        'price': price,
        'guess': guess,
        'card': card_name
    }])])
    st.session_state['guess_df'] = new_df
    st.session_state['score'] += score
    st.session_state['guesses'] += 1

def get_screen_width():
    return streamlit_js_eval(js_expressions='screen.width', key = 'SCR')

screen_width = get_screen_width()

if screen_width is None:
    screen_width = 1000

# Desktop Experience
if screen_width > 500:
    st.sidebar.image('Foil Game.png', use_column_width='always')

    if st.sidebar.button("New Card",key='New Button Sidebar'):
        st.session_state['rerun'] = True
        st.rerun()
    guess = st.sidebar.number_input('Guess the foil price in USD', value=0)
    if st.sidebar.button("Lock In", key='Lock In Sidebar'):
        st.sidebar.write('Actual Price: $' + str(int(price)))
        run_guess(price, guess, card_name)

    st.sidebar.header('Scoring')

    st.sidebar.markdown(f'''**Current Score**: ${st.session_state['score']}''')
    st.sidebar.markdown(f'''**Guesses**: {st.session_state['guesses']}''')

# Mobile Experience
else:
    st.image('Foil Game.png', use_column_width='always')
    tcol1, tcol2, tcol3 = st.columns(3)
    if tcol1.button("New Card",key='New Button'):
        st.session_state['rerun'] = True
        st.rerun()
    tcol2.markdown(f'''**Current Score**: ${st.session_state['score']}''')
    tcol3.markdown(f'''**Guesses**: {st.session_state['guesses']}''')
    col1, col2 = st.columns(2)
    guess = col1.number_input('Guess the foil price in USD', value=0)
    if col2.button("Lock In", key='Lock In'):
        st.write('Actual Price: $' + str(int(price)))
        run_guess(price, guess, card_name)

st.image(image_uri)
st.header('Guesses')
if len(st.session_state['guess_df']) > 0:
    st.scatter_chart(st.session_state['guess_df'], x='price', y='guess')
    st.dataframe(st.session_state['guess_df'])




