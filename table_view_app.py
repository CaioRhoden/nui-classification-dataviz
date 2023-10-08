import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype,
)

st.title("Auto Filter Tabela - Classificação de NUIs")

st.write(
    """Baseado em: [here](https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/)
    """
)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Adicionar Filtro")

    if not modify:
        return df

    df = df.copy()


    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Colunas a serem filtradas", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Valores para {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Intervalo para {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            else:
                user_text_input = right.text_input(
                    f"Busca para {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df


df = pd.read_csv(
    "data/results.csv"
)
st.dataframe(filter_dataframe(df))