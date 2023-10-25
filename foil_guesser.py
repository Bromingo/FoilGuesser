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

if st.session_state['rerun']:
    st.session_state['rerun'] = False
    query = 'https://api.scryfall.com/cards/random?q=set%3A7ed%20is%3Afoil'
    query_out = requests.get(query)
    content = query_out.json()
    st.session_state['content'] = content
else:
    content = st.session_state['content']

st.image('Foil Game.png', width=500)
st.write('Guess the Foil Price in USD. 7th Ed Foils are Notoriously Pricey')
# st.write(content)
image_uri = content['image_uris']['border_crop']
price_raw = content['prices']['usd_foil']
try:
    price = round(float(price_raw),0)
except:
    price = 0
    st.session_state['rerun'] = True
    st.write('No Price Found, press New Card')


mid_col1, mid_col2, mid_col3 = st.columns([2, 2,2])
if mid_col2.button("New Card"):
    st.session_state['rerun'] = True

col0, col1, col2,col3 = st.columns([1, 1, 1,2])
guess = col1.number_input('Guess the foil price in USD', value=0, label_visibility='collapsed')
img_col1, img_col2, img_col3 = st.columns(3)
if col2.button("Lock In"):
    img_col2.write('Actual Price: $' + str(int(price)))
    score = abs(guess-price)
    st.session_state['score'] += score
    st.session_state['guesses'] += 1
img_col2.image(image_uri)
