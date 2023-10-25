import streamlit as st
import pandas as pd
import numpy as np
import requests

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

#st.image('Foil Game.png', width=500)
st.sidebar.image('Foil Game.png', use_column_width='always')
# st.write(content)
image_uri = content['image_uris']['border_crop']
price_raw = content['prices']['usd_foil']
card_name = content['name']
try:
    price = round(float(price_raw),0)
except:
    price = 0
    st.session_state['rerun'] = True
    st.write('No Price Found, press New Card')


if st.sidebar.button("New Card"):
    st.session_state['rerun'] = True
guess = st.sidebar.number_input('Guess the foil price in USD', value=0)
if st.sidebar.button("Lock In"):
    st.sidebar.write('Actual Price: $' + str(int(price)))
    score = abs(guess-price)
    new_df = pd.concat([st.session_state['guess_df'],pd.DataFrame([{
        'price': price,
        'guess': guess,
        'card': card_name
    }])])
    st.session_state['guess_df'] = new_df
    st.session_state['score'] += score
    st.session_state['guesses'] += 1
    st.session_state['rerun'] = True
st.image(image_uri, width=500)
st.header('Guesses')
if len(st.session_state['guess_df']) > 0:
    st.scatter_chart(st.session_state['guess_df'], x='price', y='guess')
    st.dataframe(st.session_state['guess_df'])


st.sidebar.header('Scoring')

st.sidebar.markdown(f'''**Current Score**: ${st.session_state['score']}''')
st.sidebar.markdown(f'''**Guesses**: {st.session_state['guesses']}''')

