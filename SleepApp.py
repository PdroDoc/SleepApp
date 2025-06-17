import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import json
from streamlit_lottie import st_lottie
from streamlit_card import card


st.title("Vizualização de  Dados de Sono")
with open("cat.json") as f:
    lottie_json = json.load(f)
st_lottie(lottie_json, height=300, key="cat")


st.write("""

# Data Vizualization. Explorando dados brutos de sono.  

Bem-vindo a uma visualização interativa dos meus dados de sono, registrados pelo meu relógio **Garmin Forerunner** ao longo das últimas semanas. 

## Sobre o Projeto

Utilizando dados brutos extraídos do meu Garmin Forerunner, que monitora padrões de sono (ou a ausência deles), criei um pipeline em Python para processar e organizar essas informações em uma visualização clara e interativa. Este app, construído com **Streamlit**

## Como Funciona

1. **Coleta de Dados**: Extração de registros brutos de sono diretamente do Garmin Forerunner, incluindo tempo total de sono, fases e qualidade.
2. **Processamento**: Scripts em Python transformam os dados em formatos acessíveis, como tabelas e gráficos interativos.
3. **Visualização**: Uso do Streamlit para criar uma interface dinâmica, permitindo explorar os padrões de sono de forma intuitiva.


---

""")

st.warning("Dados das últimas 4 semanas")


col = st.columns((4, 4), gap='medium')


with st.sidebar:
        card(
        title="Pedro Potz", text="Visite meu site",image="https://taote.vercel.app/meandmiau.jpeg", url="https://pedrop.vercel.app"
)
st.sidebar.title("An app by Pedro Potz.")
st.sidebar.success("Meus Dados Sono")
#st.sidebar.info("Sleep Data App")




# Carregar CSV
sleepDF = pd.read_csv('Sleep.csv')



with st.sidebar:
# Converter coluna de data se necessário
    sleepDF["Date"] = pd.to_datetime(sleepDF["Date"], errors='coerce')



# Selectbox para escolher o dado #Selectbox
    YDadoSelect = st.selectbox(
    'Selecione um dado para visualizar',
    ["Selecione","Score", "Respiration", "Body Battery", "Resting Heart Rate","HRV Status","Pulse Ox"]
)
#Segunda opção
    #st.info("Escolha um segundo dado - opcional")
    YSecondSelect = st.selectbox(
    'Opcional:Escolha um segundo dado para visualizar',
    ["Opcional","Score", "Respiration", "Body Battery", "Resting Heart Rate","HRV Status","Pulse Ox"])

    st.info("""> Legenda.
            Score: Pontuação do sono.
            Respiration: Frequencia respiratória
            Body Battery:Bateria corporal
            Resting Heart Rate: Frequencia Cardiaca em repouso
            Pulse Ox: Oxigenação sanguinea.
            HRV Status: Variabilidade da Frequência Cardíaca""")
    st.warning(f'''>Be Aware. Dont Sleep''')




if st.checkbox("Clique para ver os dados brutos.", value=False):
       st.write(sleepDF)




# Gráfico base
base = alt.Chart(sleepDF).encode(
x="Date:T"
)


# Linha principal
linha1 = base.mark_bar(point=True).encode(
    y=alt.Y(f'{YDadoSelect}:Q', title='Valor'),
    tooltip=["Date:T", f'{YDadoSelect}:Q'],
    color=alt.value('blue')
)

# Se tiver segundo dado selecionado, cria outra linha
if YSecondSelect != 'Nenhum' and YSecondSelect != YDadoSelect:
    linha2 = base.mark_bar(point=True).encode(
        y=alt.Y(f'{YSecondSelect}:Q', title='Valor'),
        tooltip=["Date:T", f'{YSecondSelect}:Q'],
        color=alt.value('orange')
    )
    alt_chart = (linha1 + linha2).properties(
        width=700, height=400,
        title=f'Evolução de {YDadoSelect} e {YSecondSelect}'
    )
else:
    alt_chart = linha1.properties(
        width=700, height=400,
        title=f'Evolução de {YDadoSelect}'
    )
with col[0]:
# Mostrar gráfico
    st.header("Gráfico em barras")
    st.altair_chart(alt_chart, use_container_width=True)


## TESTE GRAFICO 2

with col[1]:
    st.header("Gráfico em pontos")
    linha1 = base.mark_circle(point=True).encode(
        y=alt.Y(f'{YDadoSelect}:Q', title='Valor'),
        tooltip=["Date:T", f'{YDadoSelect}:Q'],
        color=alt.value('red')
    )

    if YSecondSelect != 'Nenhum' and YSecondSelect != YDadoSelect:
        linha2 = base.mark_circle(point=True).encode(
            y=alt.Y(f'{YSecondSelect}:Q', title='Valor'),
            tooltip=["Date:T", f'{YSecondSelect}:Q'],
            color=alt.value('blue')
        )
        alt_chart = (linha1 + linha2).properties(
            width=700, height=400,
            title=f'Evolução de {YDadoSelect} e {YSecondSelect}'
        )
    else:
        alt_chart = linha1.properties(
            width=700, height=400,
            title=f'Evolução de {YDadoSelect}'
        )
    with col[1]:
        # Mostrar gráfico
        st.altair_chart(alt_chart, use_container_width=True)

    ## Usando o maplottlip

    #st.header("Outras Métricas e Gráficos")



    #fig, ax = plt.subplots()

    #ax.plot(sleepDF['Date'], sleepDF[YDadoSelect], label=YDadoSelect)
    #ax.plot(sleepDF['Date'],sleepDF[YSecondSelect], label=YSecondSelect)

    #ax.set_xlabel("Data")
    #ax.set_ylabel("Valor")
    #ax.legend()

    #st.pyplot(fig)

#-----
sleepDF['Score'] = pd.to_numeric(sleepDF['Score'], errors='coerce')
ScMean =round(sleepDF['Score'].mean(), 2)
ScMin = round(sleepDF['Score'].min(), 2)
ScMax = round(sleepDF['Score'].max(), 2)
ScModa = round(sleepDF['Score'].mode(), 2)
ScMedian = round(sleepDF['Score'].median(), 2)

if st.checkbox("Ver métricas da pontuação de sono ?", value=False):
    st.warning(f'''Métrica daPontuação de qualidade do meu Sono nas últimas 4 Semanas:
      
        Pontuação Mínima: {ScMin:.2f}
        Pontuação Máxima: {ScMax:.2f}
          Pontuação Média: {ScMean:.2f}
        Mediana da Pontuação: {ScMedian:.2f}
        Dias sem dormir no período: 15 Dias. 🙀''')




### Outro grafico


# Cria eixo X (pode ser data ou índice)
x = 'Date'
# Cria a figura
fig, ax = plt.subplots()


# Plota os Scores reais (linha azul)
##plt.plot(x, df['Score'], label='Score Diário', marker='o')
##plt.stem(values, markerfmt=' ')
(markers, stemlines, baseline) = plt.stem(sleepDF['Score'])
plt.setp(markers, marker='D', markersize=10, markeredgecolor="orange", markeredgewidth=2)
# Plota linhas horizontais para as métricas
plt.axhline(ScMean, color='green', linestyle='--', label=f'Média {ScMean}')
plt.axhline(ScMin, color='red', linestyle='--', label=f'Mínimo {ScMin}')
plt.axhline(ScMax, color='purple', linestyle='--', label=f'Máximo {ScMax}')
#plt.axhline(ScModa, color='orange', linestyle='--', label=f'Moda {ScModa}')
plt.axhline(ScMedian, color='cyan', linestyle='--', label=f'Mediana {ScMedian}')

# Ajustes visuais
plt.title('Score de Sono com Métricas')
plt.xlabel('Dias')
plt.ylabel('Score')
plt.legend()
plt.grid(True)
plt.tight_layout()
if st.checkbox("Ver gráfico da metrica ?", value=False):
    st.header("Muito mais fácil assim, né?")
    st.pyplot(fig)
