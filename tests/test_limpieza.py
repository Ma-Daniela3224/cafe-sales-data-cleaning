"""
Tests unitarios para el modulo de limpieza de datos.

Cada test crea un DataFrame pequeno e inventado, donde sabemos exactamente 
cual deberia ser el resultado correcto, y verificamos que la funcion lo 
produzca.
"""

import pandas as pd
import sys
import os

# Permite importar src/limpieza.py desde la carpeta tests/
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from limpieza import (
    estandarizar_valores_sucios,
    convertir_tipos,
    recuperar_valores_numericos,
    imputar_categoricas,
    eliminar_filas_irrecuperables,
)


def test_estandarizar_valores_sucios():
    """ERROR y UNKNOWN deben convertirse en NaN real."""
    df = pd.DataFrame({'Item': ['Coffee', 'ERROR', 'UNKNOWN', 'Cake']})
    resultado = estandarizar_valores_sucios(df)

    assert resultado['Item'].isnull().sum() == 2
    assert resultado['Item'].iloc[0] == 'Coffee'


def test_convertir_tipos():
    """Las columnas numericas y de fecha deben convertirse correctamente."""
    df = pd.DataFrame({
        'Quantity': ['2', '3', 'no_es_numero'],
        'Price Per Unit': ['1.5', '2.0', '3.0'],
        'Total Spent': ['3.0', '6.0', '9.0'],
        'Transaction Date': ['2023-01-01', '2023-01-02', 'fecha_invalida'],
    })
    resultado = convertir_tipos(df)

    assert resultado['Quantity'].dtype == 'float64'
    assert pd.api.types.is_datetime64_any_dtype(resultado['Transaction Date'])
    # El valor invalido debe convertirse en NaN, no causar error
    assert pd.isnull(resultado['Quantity'].iloc[2])


def test_recuperar_valores_numericos():
    """Debe recuperar Total Spent usando Quantity * Price Per Unit."""
    df = pd.DataFrame({
        'Quantity': [2.0, 3.0],
        'Price Per Unit': [5.0, 4.0],
        'Total Spent': [None, 12.0],  # el primero falta, el segundo ya existe
    })
    resultado = recuperar_valores_numericos(df)

    # 2.0 * 5.0 = 10.0, debe haberse calculado
    assert resultado['Total Spent'].iloc[0] == 10.0
    # el segundo ya tenia valor, no debe cambiar
    assert resultado['Total Spent'].iloc[1] == 12.0


def test_imputar_categoricas():
    """Los nulos en columnas categoricas deben rellenarse con 'Not Specified'."""
    df = pd.DataFrame({
        'Item': ['Coffee', None],
        'Payment Method': [None, 'Cash'],
        'Location': ['In-store', None],
    })
    resultado = imputar_categoricas(df)

    assert resultado.isnull().sum().sum() == 0
    assert resultado['Item'].iloc[1] == 'Not Specified'


def test_eliminar_filas_irrecuperables():
    """Debe eliminar solo las filas donde los tres valores numericos son NaN."""
    df = pd.DataFrame({
        'Quantity': [2.0, None],
        'Price Per Unit': [5.0, None],
        'Total Spent': [10.0, None],
    })
    resultado = eliminar_filas_irrecuperables(df)

    assert resultado.shape[0] == 1
    assert resultado['Total Spent'].iloc[0] == 10.0
    