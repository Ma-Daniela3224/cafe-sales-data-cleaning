"""
Modulo de limpieza para el dataset Dirty Cafe Sales.

Convierte el dataset original "sucio" (con valores ERROR/UNKNOWN, nulos y 
tipos de dato incorrectos) en un dataset limpio y listo para analisis.
"""

import pandas as pd


def cargar_datos(ruta_csv):
    """Carga el CSV original sin procesar."""
    return pd.read_csv(ruta_csv)


def estandarizar_valores_sucios(df):
    """Convierte 'ERROR' y 'UNKNOWN' a NaN real."""
    df = df.replace(['ERROR', 'UNKNOWN'], pd.NA)
    return df


def convertir_tipos(df):
    """Convierte columnas a sus tipos de dato correctos."""
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Price Per Unit'] = pd.to_numeric(df['Price Per Unit'], errors='coerce')
    df['Total Spent'] = pd.to_numeric(df['Total Spent'], errors='coerce')
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
    return df


def recuperar_valores_numericos(df):
    """
    Recupera valores faltantes en Quantity, Price Per Unit y Total Spent 
    usando la relacion: Total Spent = Quantity * Price Per Unit
    """
    # Recupera Total Spent
    calculado_total = df['Quantity'] * df['Price Per Unit']
    df['Total Spent'] = df['Total Spent'].fillna(calculado_total)

    # Recupera Price Per Unit
    calculado_precio = df['Total Spent'] / df['Quantity']
    df['Price Per Unit'] = df['Price Per Unit'].fillna(calculado_precio)

    # Recupera Quantity
    calculado_cantidad = df['Total Spent'] / df['Price Per Unit']
    df['Quantity'] = df['Quantity'].fillna(calculado_cantidad)

    return df


def imputar_categoricas(df):
    """Rellena nulos en columnas categoricas con una etiqueta explicita."""
    df['Item'] = df['Item'].fillna('Not Specified')
    df['Payment Method'] = df['Payment Method'].fillna('Not Specified')
    df['Location'] = df['Location'].fillna('Not Specified')
    return df


def eliminar_filas_irrecuperables(df):
    """Elimina filas donde no fue posible recuperar Quantity, Price Per Unit o Total Spent."""
    df = df.dropna(subset=['Quantity', 'Price Per Unit', 'Total Spent'])
    return df


def limpiar_dataset(ruta_csv):
    """
    Ejecuta el flujo completo de limpieza sobre el dataset original.

    Parametros:
        ruta_csv (str): ruta al archivo CSV original (sucio)

    Retorna:
        pd.DataFrame: dataset limpio
    """
    df = cargar_datos(ruta_csv)
    df = estandarizar_valores_sucios(df)
    df = convertir_tipos(df)
    df = recuperar_valores_numericos(df)
    df = imputar_categoricas(df)
    df = eliminar_filas_irrecuperables(df)
    return df


if __name__ == '__main__':
    # Permite correr este script directamente desde terminal:
    # python src/limpieza.py
    df_limpio = limpiar_dataset('data/dirty_cafe_sales.csv')
    df_limpio.to_csv('data/cafe_sales_clean.csv', index=False)
    print(f'Dataset limpio guardado: {df_limpio.shape[0]} filas, {df_limpio.shape[1]} columnas')
    