import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
def mostrar_indicador_financiero(titulo, formula, descripcion):
    st.header(titulo)

    col1, col2, col3 = st.columns(3)

    col1.subheader("Fórmula:")
    col1.write(formula)

    col2.subheader("Descripción:")
    col2.write(descripcion)

# Leer los datos
dfROA = pd.read_csv("formulascsvFINAL1.csv")

# Menú desplegable para agrupar las fórmulas
selected_group = st.sidebar.selectbox("Selecciona un grupo", ["Formulas 1", "Formulas 2"])

# Mostrar el menú de selección de fórmulas solo cuando se selecciona el grupo "Formulas 1"
if selected_group == "Formulas 1":
    # Menú de selección entre las fórmulas
    selected_formula = st.sidebar.selectbox("Selecciona una fórmula", [
        "ROA por Trimestre",
        "Gasto Operativo por Trimestre",
        "Solvencia Patrimonial"
    ])
# Mostrar la fórmula seleccionada
    if selected_formula == "ROA por Trimestre":
        mostrar_indicador_financiero(
            "Rentabilidad sobre el activo (ROA)",
            "ROA = Utilidad Neta / Activos Totales Promedio",
            "Esta fórmula mide la eficiencia con la que una empresa utiliza sus activos para generar ganancias."
        )

        # Calcular ROA por trimestre
        dfROA['SALDO'] = pd.to_numeric(dfROA['SALDO'].replace('[\$,]', '', regex=True), errors='coerce')
        dfROA['FECHA'] = pd.to_datetime(dfROA['FECHA'], format='%m/%d/%Y')
        dfROA['AÑO'] = dfROA['FECHA'].dt.year
        dfROA['ROA'] = dfROA.groupby('AÑO')['SALDO'].pct_change(4) * 100

        fig_roa = make_subplots(rows=1, cols=1, shared_xaxes=True)

        df_filtered_roa = dfROA.dropna(subset=['ROA'])

        for year in df_filtered_roa['AÑO'].unique():
            data_year = df_filtered_roa[df_filtered_roa['AÑO'] == year]
            fig_roa.add_trace(go.Scatter(x=data_year['FECHA'], y=data_year['ROA'], mode='lines+markers', name=f'ROA - {year}'))

        fig_roa.update_layout(title='ROA por Trimestre',
                            xaxis_title='Fecha',
                            yaxis_title='ROA')

        st.subheader("Gráfico de ROA por Trimestre")
        st.plotly_chart(fig_roa)

        dfROA['AÑO'] = dfROA['FECHA'].dt.year

        # Calcular ROA por trimestre
        dfROA['ROA'] = dfROA.groupby('AÑO')['SALDO'].pct_change(4) * 100

        # Filtrar solo los datos que tienen ROA (descartando NaN)
        df_filtered = dfROA.dropna(subset=['ROA'])

        # Crear gráfico interactivo de dispersión animado para ROA por trimestre y año
        fig_animated_scatter_roa = px.scatter(df_filtered, x='FECHA', y='ROA', animation_frame='AÑO',
                                            labels={'ROA': 'ROA (%)', 'FECHA': 'Fecha'},
                                            title='Variación del ROA por Trimestre y Año',
                                            range_x=[dfROA['FECHA'].min(), dfROA['FECHA'].max()],
                                            range_y=[df_filtered['ROA'].min(), df_filtered['ROA'].max()])
        st.subheader("Gráfico de la evolucion de ROA")
        st.plotly_chart(fig_animated_scatter_roa)

        ingresos = dfROA[dfROA['TIPO'] == 5].groupby('FECHA')['SALDO'].sum()
        gastos = dfROA[dfROA['TIPO'] == 4].groupby('FECHA')['SALDO'].sum()
        roa = (ingresos - gastos) / dfROA[dfROA['TIPO'] == 1].groupby('FECHA')['SALDO'].mean() * 100

        fig = px.line(roa, x=roa.index, y='SALDO', title='ROA a lo largo del tiempo')
        fig.update_xaxes(title_text='Fecha')
        fig.update_yaxes(title_text='ROA (%)')

        st.subheader("Gráfico de ROA a lo largo del tiempo")
        st.plotly_chart(fig)

    elif selected_formula == "Gasto Operativo por Trimestre":
        mostrar_indicador_financiero(
            "Eficiencia en Gasto Operativo",
            "Eficiencia en Gasto Operativo = (Ingresos Totales - Gasto Operativo) / Ingresos Totales",
            "Evalúa qué tan eficientemente una empresa está administrando sus gastos operativos en relación con sus ingresos. Un valor más alto indica mayor eficiencia."
        )

        # Convertir la columna 'SALDO' a tipo numérico
        dfROA['SALDO'] = pd.to_numeric(dfROA['SALDO'].replace('[\$,]', '', regex=True), errors='coerce')

        # Convertir la columna 'FECHA' a tipo datetime
        dfROA['FECHA'] = pd.to_datetime(dfROA['FECHA'], format='%m/%d/%Y')

        # Crear una nueva columna para el año
        dfROA['AÑO'] = dfROA['FECHA'].dt.year

        # Calcular Gasto Operativo por trimestre
        dfROA['GASTO_OPERATIVO'] = dfROA[dfROA['NombreCuenta'] == 'GASTOS DE OPERACION'].groupby('AÑO')['SALDO'].pct_change(4) * 100

        # Crear un gráfico interactivo con una línea por cada año para Gasto Operativo
        fig_gasto_operativo = make_subplots(rows=1, cols=1, shared_xaxes=True)

        # Filtrar solo los datos que tienen Gasto Operativo (descartando NaN)
        df_filtered_gasto_operativo = dfROA.dropna(subset=['GASTO_OPERATIVO'])

        for year in df_filtered_gasto_operativo['AÑO'].unique():
            data_year = df_filtered_gasto_operativo[df_filtered_gasto_operativo['AÑO'] == year]
            fig_gasto_operativo.add_trace(go.Scatter(x=data_year['FECHA'], y=data_year['GASTO_OPERATIVO'], mode='lines+markers', name=f'Gasto Operativo - {year}'))

        # Actualizar diseño del gráfico Gasto Operativo
        fig_gasto_operativo.update_layout(title='Gasto Operativo por Trimestre',
                                        xaxis_title='Fecha',
                                        yaxis_title='Gasto Operativo')
        st.subheader("Gráfico de Gasto Operativo por Trimestre")
        st.plotly_chart(fig_gasto_operativo)
        gastos_operativos = dfROA[dfROA['NombreCuenta'] == 'GASTOS DE OPERACION']
        fig = px.bar(gastos_operativos, x='FECHA', y='SALDO', color='GRUPO',
                    labels={'SALDO': 'Gasto Operativo', 'GRUPO': 'Categoría'},
                    title='Desglose del Gasto Operativo por Categoría a lo largo del tiempo')
        fig.update_xaxes(title_text='Fecha')
        fig.update_yaxes(title_text='Gasto Operativo')
        st.subheader("Gráfico de barras de Gasto Operativo")
        st.plotly_chart(fig)

        gastos_operativos = dfROA[dfROA['NombreCuenta'] == 'GASTOS DE OPERACION'].groupby('FECHA')['SALDO'].sum()

        fig = px.line(gastos_operativos, x=gastos_operativos.index, y='SALDO', title='Gasto Operativo a lo largo del tiempo')
        fig.update_xaxes(title_text='Fecha')
        fig.update_yaxes(title_text='Gasto Operativo')
        st.subheader("Gráfico de Gasto Operativo a lo largo del tiempo")
        st.plotly_chart(fig)

    elif selected_formula == "Solvencia Patrimonial":
        mostrar_indicador_financiero(
            "Solvencia Patrimonial",
            "Solvencia = Patrimonio / Activos Totales",
            "Mide la proporción del patrimonio en relación con los activos totales, indicando el nivel de seguridad financiera y la capacidad para absorber pérdidas."
        )

        # Convertir la columna 'SALDO' a tipo numérico
        dfROA['SALDO'] = pd.to_numeric(dfROA['SALDO'].replace('[\$,]', '', regex=True), errors='coerce')

        # Convertir la columna 'FECHA' a tipo datetime
        dfROA['FECHA'] = pd.to_datetime(dfROA['FECHA'], format='%m/%d/%Y')

        # Crear una nueva columna para el año
        dfROA['AÑO'] = dfROA['FECHA'].dt.year

        # Calcular Solvencia Patrimonial
        df_solvencia = dfROA.pivot(index='FECHA', columns='NombreCuenta', values='SALDO').reset_index()
        df_solvencia['SOLVENCIA_PATRIMONIAL'] = df_solvencia['PATRIMONIO'] / df_solvencia['ACTIVO'] * 100

        # Crear un gráfico interactivo
        fig_solvencia = make_subplots(rows=1, cols=1, shared_xaxes=True)

        # Añadir la línea de Solvencia Patrimonial al gráfico
        fig_solvencia.add_trace(go.Scatter(x=df_solvencia['FECHA'], y=df_solvencia['SOLVENCIA_PATRIMONIAL'], mode='lines+markers', name='Solvencia Patrimonial'))

        # Actualizar diseño del gráfico
        fig_solvencia.update_layout(title='Solvencia Patrimonial',
                                    xaxis_title='Fecha',
                                    yaxis_title='Solvencia Patrimonial (%)')

        # Mostrar el gráfico
        st.subheader("Gráfico de Solvencia Patrimonial")
        st.plotly_chart(fig_solvencia)
        solvencia = dfROA[dfROA['TIPO'].isin([1, 3])] 
        solvencia['SOLVENCIA_PATRIMONIAL'] = solvencia.groupby(['FECHA', 'NombreCuenta'])['SALDO'].transform('sum')
        fig_solvencia = px.line(solvencia, x='FECHA', y='SOLVENCIA_PATRIMONIAL', color='NombreCuenta',
                                labels={'SOLVENCIA_PATRIMONIAL': 'Solvencia Patrimonial', 'NombreCuenta': 'Cuenta'},
                                title='Solvencia Patrimonial a lo largo del tiempo')
        fig_solvencia.update_xaxes(title_text='Fecha')
        fig_solvencia.update_yaxes(title_text='Monto')
        st.subheader("Gráfico comparativa de activo y patrimonio de Solvencia Patrimonial")
        st.plotly_chart(fig_solvencia)
elif selected_group == "Formulas 2":
    st.header("Fórmulas de prueba para el grupo Formulas 2")

    # Menú de selección para el grupo "Formulas 2"
    selected_formula_group2 = st.sidebar.selectbox("Selecciona una fórmula", [
        "Fórmula de Prueba 1",
        "Fórmula de Prueba 2"
    ])

    # Mostrar la fórmula seleccionada para el grupo "Formulas 2"
    if selected_formula_group2 == "Fórmula de Prueba 1":
        st.subheader("Fórmula de Prueba 1")
        st.write("Esta es una fórmula de prueba para el grupo Formulas 2.")

        # Gráfico de prueba
        data = {'X': np.arange(10), 'Y': np.random.rand(10)}
        df_test = pd.DataFrame(data)
        fig_test = px.scatter(df_test, x='X', y='Y', title='Gráfico de prueba para Fórmula de Prueba 1')
        st.plotly_chart(fig_test)

    elif selected_formula_group2 == "Fórmula de Prueba 2":
        st.subheader("Fórmula de Prueba 2")
        st.write("Otra fórmula de prueba para el grupo Formulas 2.")

        # Otro gráfico de prueba
        data = {'X': np.arange(10), 'Y': np.random.rand(10)}
        df_test = pd.DataFrame(data)
        fig_test = px.line(df_test, x='X', y='Y', title='Gráfico de prueba para Fórmula de Prueba 2')
        st.plotly_chart(fig_test)
