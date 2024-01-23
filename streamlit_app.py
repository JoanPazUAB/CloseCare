import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import altair as alt
import streamlit as st
 

def check_outliers(df, column_name, start_date, end_date, rolling_period, sensitivity=1.5):
    # Filtrar el DataFrame según el rango de fechas
    df_filtered = df[(df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)]

    # Calcular los cuantiles de la columna completa
    q1_full = df['Columna'].quantile(0.25)
    q3_full = df['Columna'].quantile(0.75)

    # Calcular la media para grupos de tres valores
    df_filtered['Media_Periodo'] = df_filtered['Columna'].rolling(window=rolling_period, min_periods=1).mean()

    # Seleccionar el último valor de cada grupo de tres
    # df_result = df_filtered.groupby(df_filtered.index // rolling_period).tail(1)
    # Suponiendo que 'Fecha' es una columna de tipo datetime en df_filtered
    df_result = df_filtered.groupby(df_filtered.index // rolling_period).apply(lambda group: group.tail(1) if len(group) % rolling_period == 0 else pd.DataFrame())
    df_result.reset_index(drop=True, inplace=True)

    if rolling_period != 1:
        df_result['Fecha'] = df_result['Fecha'].apply(lambda date: f"{(date - timedelta(days=rolling_period-1)).strftime('%Y-%m-%d')} - {date.strftime('%Y-%m-%d')}")

    # Calcular el rango intercuartílico (IQR)
    iqr = q3_full - q1_full

    # Definir umbrales para identificar outliers
    lower_threshold = q1_full - sensitivity * iqr
    upper_threshold = q3_full + sensitivity * iqr

    st.write(f'{lower_threshold} - {upper_threshold}')

    # Identificar outliers
    df_outliers = df_result[(df_result['Media_Periodo'] < lower_threshold) | (df_result['Media_Periodo'] > upper_threshold)]

    # Agregar el intervalo de fechas al DataFrame de outliers usando .loc[]

    # Restar 3 días
    # for date in df_outliers['Fecha']:
    #     df_outliers['Fecha'][df_outliers['Fecha']==date] = "{} - {}".format(date - timedelta(days=rolling_period-1), date)


    return df_result, df_outliers, lower_threshold, upper_threshold

# def plot_outliers(df_result, lower_threshold, upper_threshold):
#     # Crear un gráfico de dispersión con líneas de tendencia y umbrales sombreados
#     chart = alt.Chart(df_result).mark_point().encode(
#         x='Fecha:T',
#         y='Media_Periodo:Q',
#         tooltip=['Fecha:T', 'Media_Periodo:Q']
#     ).properties(width=600, height=400)

#     # Línea de tendencia
#     trendline = chart.transform_regression('Fecha', 'Media_Periodo').mark_line()

#     # Líneas de umbrales
#     lower_threshold_line = alt.Chart(pd.DataFrame({'threshold': [lower_threshold]})).mark_rule(color='red', strokeWidth=2).encode(y='threshold:Q')
#     upper_threshold_line = alt.Chart(pd.DataFrame({'threshold': [upper_threshold]})).mark_rule(color='red', strokeWidth=2).encode(y='threshold:Q')

#     # Sombreado entre umbrales
#     shaded_area = alt.Chart(df_result).mark_area(opacity=0.3, color='red').encode(
#         x='Fecha:T',
#         y='lower_threshold:Q',
#         y2='upper_threshold:Q'
#     ).transform_calculate(
#         lower_threshold=f"{lower_threshold}",
#         upper_threshold=f"{upper_threshold}"
#     )

#     # Combinar todos los elementos
#     chart = (chart + trendline + lower_threshold_line + upper_threshold_line + shaded_area).properties(
#         title='Gráfico de Outliers',
#         xlabel='Intervalo de Fechas',
#         ylabel='Media_Periodo'
#     )

#     return chart

def plot_outliers(df_result, lower_threshold, upper_threshold):
    # Crear un gráfico de dispersión con líneas de tendencia y umbrales sombreados
    chart = alt.Chart(df_result).mark_point().encode(
        x='Fecha:T',
        y='Media_Periodo:Q',
        tooltip=['Fecha:T', 'Media_Periodo:Q']
    ).properties(width=600, height=400)

    # Línea de tendencia
    trendline = chart.transform_regression('Fecha', 'Media_Periodo').mark_line()

    # Líneas de umbrales
    lower_threshold_line = alt.Chart(pd.DataFrame({'threshold': [lower_threshold]})).mark_rule(color='red', strokeWidth=2).encode(y='threshold:Q')
    upper_threshold_line = alt.Chart(pd.DataFrame({'threshold': [upper_threshold]})).mark_rule(color='red', strokeWidth=2).encode(y='threshold:Q')

    # Sombreado entre umbrales
    shaded_area = alt.Chart(df_result).mark_area(opacity=0.3, color='red').encode(
        x='Fecha:T',
        y='lower_threshold:Q',
        y2='upper_threshold:Q'
    ).transform_calculate(
        lower_threshold=f"{lower_threshold}",
        upper_threshold=f"{upper_threshold}"
    )

    # Combinar todos los elementos
    chart = (chart + trendline + lower_threshold_line + upper_threshold_line + shaded_area).properties(
        title='Gráfico de Outliers'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    return chart

# Ejemplo de uso
# df = pd.DataFrame({
#     'Fecha': pd.date_range(start='2022-01-01', periods=10),
#     'Columna': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# })
data = {
        'Fecha': pd.date_range(start='2022-01-01', end='2024-01-10'),
        'Columna': np.random.normal(loc=10, scale=2, size=len(pd.date_range(start='2022-01-01', end='2024-01-10')))
    }
df = pd.DataFrame(data)
df.loc[df.index[-1], 'Columna'] = 1000
start_date = '2022-01-01'
end_date = '2024-01-10'
rolling_period = 3

# Ajusta la sensibilidad según tus necesidades
sensitivity = 0

df_result, df_outliers, low, up = check_outliers(df, 'Columna', start_date, end_date, rolling_period, sensitivity)



# Mostrar los resultados
# print('Resultados del Chequeo de Outliers:')
st.write(df_result)
# print('Outliers Identificados:')
st.write(df_outliers)

#st.write(f"Streamlit version: {st.__version__}")
#st.write(f"Altair version: {alt.__version__}")

#chart = plot_outliers(df_result, low, up)
#st.write(chart)
#st.altair_chart(chart, use_container_width=True)

chart = alt.Chart().mark_point().encode(x='date:T', y='value:Q').properties(width=600, height=400)
st.altair_chart(chart, use_container_width=True)
