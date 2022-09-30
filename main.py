import numpy as np
import pandas as pd
import requests

import streamlit as st

from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)

df = pd.read_csv('C:/Users/cankemaloglu/PycharmProjects/DSMLBC-8/1. Part/persona.csv')

agg_df = df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()

agg_df.reset_index(inplace=True)
agg_df.head()

bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]
agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()

agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

agg_df = agg_df[["customers_level_based","PRICE"]]
agg_df.head()

## Price a göre segmentasyon

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})

## Segment tekilleştirme
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df.head()

agg_df = agg_df.reset_index()
agg_df.head()





st.set_page_config(page_title="Gamer Price Guess App", page_icon=":space_invader:")

@st.cache

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url_hello = "https://assets3.lottiefiles.com/packages/lf20_EHLDNO3O5W.json"
lottie_url_country = "https://assets6.lottiefiles.com/private_files/lf30_ahlkj7sh.json"
lottie_url_source = "https://assets2.lottiefiles.com/packages/lf20_l3qxn9jy.json"
lottie_url_gender = "https://assets7.lottiefiles.com/packages/lf20_cSNnXm5euH.json"
lottie_url_age = "https://assets9.lottiefiles.com/packages/lf20_0aRzimjEMW.json"

lottie_hello = load_lottieurl(lottie_url_hello)
lottie_country = load_lottieurl(lottie_url_country)
lottie_source = load_lottieurl(lottie_url_source)
lottie_gender = load_lottieurl(lottie_url_gender)
lottie_age = load_lottieurl(lottie_url_age)

col1, col2= st.columns(2)
with col1:
    st_lottie(lottie_hello, key="hello")

with col2:
    st.title('How much a gamer spending ?')


col_c_ani, col_s_ani, col_g_ani, col_a_ani = st.columns(4)

with col_c_ani:
    st_lottie(lottie_country, height=100, width=160)
with col_s_ani:
    st_lottie(lottie_source, height=100, width=160)
with col_g_ani:
    st_lottie(lottie_gender, height=100, width=160)
with col_a_ani:
    st_lottie(lottie_age, height=100, width=160)



col_c, col_s, col_g, col_a = st.columns(4)
with col_c:
    country_name = st.selectbox(
        "Select Country",
        (df["COUNTRY"].unique())
    )
with col_s:
    source_name = st.selectbox(
        "Select Source",
        (df["SOURCE"].unique())
    )
with col_g:
    gender_name = st.selectbox(
        "Select Gender",
        (df["SEX"].unique())
    )
with col_a:
    age_cat_choice = st.selectbox(
        "Select Age Category",
        (mylabels)
)

#st.write(country_name.upper() + "_" + source_name.upper() + "_" + gender_name.upper() + "_" + age_cat_choice)

## Yeni Gelen Müşterileri Sınıflandırma ve Gelir Tahmini


if st.button("Guess Price"):
    new_user = f"{country_name.upper()}_{source_name.upper()}_{gender_name.upper()}_{age_cat_choice}"
    #new_user = "TUR_ANDROID_FEMALE_41_66"
    #st.write(new_user, agg_df[agg_df["customers_level_based"] == new_user])
    #st.balloons()
    agg_df[agg_df["customers_level_based"] == new_user]





