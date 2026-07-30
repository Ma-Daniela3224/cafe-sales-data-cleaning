"""
Dashboard interactivo para explorar el dataset limpio de ventas de cafeteria.

Ejecutar con: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuracion de la pagina ---
st.set_page_config(page_title="Cafe Sales Dashboard", page_icon="☕", layout="wide")

# --- Carga de datos ---
@st.cache_data
def cargar_datos():
    df = pd.read_csv('data/cafe_sales_clean.csv')
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
    return df

df = cargar_datos()

# --- Titulo ---
st.title("☕ Dashboard de Ventas de Cafeteria")
st.markdown("Explora el dataset limpio de forma interactiva. Datos originales de [Kaggle - Dirty Cafe Sales](https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training).")

# --- Filtros en la barra lateral ---
st.sidebar.header("Filtros")

productos = st.sidebar.multiselect(
    "Producto",
    options=sorted(df['Item'].unique()),
    default=sorted(df['Item'].unique())
)

metodos_pago = st.sidebar.multiselect(
    "Metodo de pago",
    options=sorted(df['Payment Method'].unique()),
    default=sorted(df['Payment Method'].unique())
)

ubicaciones = st.sidebar.multiselect(
    "Ubicacion",
    options=sorted(df['Location'].unique()),
    default=sorted(df['Location'].unique())
)

# --- Aplicar filtros ---
df_filtrado = df[
    (df['Item'].isin(productos)) &
    (df['Payment Method'].isin(metodos_pago)) &
    (df['Location'].isin(ubicaciones))
]

# --- Metricas principales ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Transacciones", f"{df_filtrado.shape[0]:,}")
col2.metric("Ventas totales", f"${df_filtrado['Total Spent'].sum():,.2f}")
col3.metric("Ticket promedio", f"${df_filtrado['Total Spent'].mean():.2f}")
col4.metric("Producto top", df_filtrado['Item'].value_counts().idxmax() if not df_filtrado.empty else "N/A")

st.divider()

# --- Graficas en dos columnas ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Transacciones por producto")
    fig, ax = plt.subplots(figsize=(6, 4))
    conteo_items = df_filtrado['Item'].value_counts()
    sns.barplot(x=conteo_items.values, y=conteo_items.index, hue=conteo_items.index,
                palette='viridis', legend=False, ax=ax)
    ax.set_xlabel("Numero de transacciones")
    st.pyplot(fig)

with col_der:
    st.subheader("Transacciones por metodo de pago")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    conteo_pago = df_filtrado['Payment Method'].value_counts()
    sns.barplot(x=conteo_pago.values, y=conteo_pago.index, hue=conteo_pago.index,
                palette='mako', legend=False, ax=ax2)
    ax2.set_xlabel("Numero de transacciones")
    st.pyplot(fig2)

st.divider()

# --- Tabla de datos ---
st.subheader("Datos filtrados")
st.dataframe(df_filtrado, use_container_width=True)
