import streamlit as st
import pandas as pd
from pandas import read_csv

# Chave única para cada widget
widget_key1 = "selectbox1"
widget_key2 = "selectbox2"

st.set_page_config(page_title="Mapa CSA App")

def normaliza_1(valor):      
   valor_f = float(valor.replace(',', '.')) - 0   
   valor_n = (valor_f - 0)/(100 - 0)
   return round(valor_n, 3)

def normaliza_2(valor):      
   valor_f = float(valor.replace(',', '.')) - 0
   valor_n = (valor_f - 0)/(5 - 0)
   return round(valor_n, 3)

def extrai_fator_motivacional(fatores, tipo):      
   partes = fatores.split(",")   
   valor = partes[int(tipo)].split("(")[1].split(")")[0]                    
   return valor
  
def extrai_ea_fa(ea_fa):   
   partes = ea_fa.split(" ")
   ea_fa = partes[0]
   valor = partes[1].strip("()")
   return ea_fa, valor

def extrai_aspecto_social(as_interacao):   
   if "+" in as_interacao:
      valor = as_interacao.split("+")
   else:
      valor = [as_interacao]
   valor = [valor.strip() for valor in valor]   
   return valor
   
      



# INFERÊNCIA DA CSA RESILIÊNCIA
def infere_resiliencia(confianca, esforco, aa_estado_animo, aa_familia_afetiva, tp_realizacao, tp_abertura, independencia, as_interacao):   
   estado_animo = 0
   familia_afetiva = 0
   confianca_n = 0
   esforco_n = 0
   independencia_n = 0
   valor_estado_animo_n = 0
   valor_familia_afetiva_n = 0
   
   if confianca != 0:
    confianca_n = normaliza_1(confianca) 
   
   if esforco != 0:
    esforco_n = normaliza_1(esforco)
   
   if independencia != 0:
    independencia_n = normaliza_1(independencia)   

   if aa_estado_animo != 0:
      estado_animo, valor_estado_animo = extrai_ea_fa(aa_estado_animo)
      valor_estado_animo_n = normaliza_2(valor_estado_animo)

   if aa_familia_afetiva != 0:
      familia_afetiva, valor_familia_afetiva = extrai_ea_fa(aa_familia_afetiva)
      valor_familia_afetiva_n = normaliza_2(valor_familia_afetiva)
   
   realizacao_n = normaliza_1(str(tp_realizacao))
   abertura_n = normaliza_1(str(tp_abertura))

   peso_ea = 0.0
   peso_fa = 0.0

   if estado_animo == "animado":
      peso_ea = 0.107
   if estado_animo == "satisfeito":
      peso_ea = 0.063   

   if familia_afetiva == "entusiasmo":
      peso_fa = 0.083
   if familia_afetiva == "interesse":
      peso_fa = 0.069
   if familia_afetiva == "serenidade":
      peso_fa = 0.069
   if familia_afetiva == "esperança":
      peso_fa = 0.065
   if familia_afetiva == "orgulho":
      peso_fa = 0.055           

   if "colaboração" in as_interacao:      
      as_interacao = 1
   else:
      as_interacao = 0             

   st.write("confiança:", confianca_n)
   st.write("esforço:", esforco_n) 
   st.write("independência:", independencia_n)
   st.write(estado_animo, valor_estado_animo_n)
   st.write(familia_afetiva, valor_familia_afetiva_n)
   st.write("realização:", realizacao_n)
   st.write("abertura:", abertura_n)
   st.write("colaboração:", as_interacao)

   if confianca_n > 0:
      confianca_n = (confianca_n * 0.202) + 0.04

   if esforco_n > 0:
      esforco_n = (esforco_n * 0.113) + 0.04

   if independencia_n > 0:
      independencia_n = (independencia_n * 0.034) + 0.04

   if valor_estado_animo_n > 0:
      valor_estado_animo_n = (valor_estado_animo_n * peso_ea) + 0.04

   if valor_familia_afetiva_n > 0:
      valor_familia_afetiva_n = (valor_familia_afetiva_n * peso_fa) + 0.04

   if realizacao_n > 0:
      realizacao_n = (realizacao_n * 0.069) + 0.04

   if abertura_n > 0:
      abertura_n = (abertura_n * 0.048) + 0.04

   if as_interacao > 0:
      as_interacao = (as_interacao * 0.024) + 0.04

   resiliencia = confianca_n + esforco_n + valor_estado_animo_n + valor_familia_afetiva_n + realizacao_n + abertura_n + independencia_n + as_interacao
   st.write("RESILIÊNCIA:", f"{resiliencia:.3f}")     


def pagina_inicio():
    st.title("Mapa CSA App")
    st.write("Este app infere e mostra as competências socioafetivas de estudantes.")
    nome = st.text_input("Digite seu nome:")
    if st.button("Entrar") and len(nome)>0:
        st.session_state["nome"] = nome        
        st.rerun()
    st.write("Para mais informações sobre como o app funciona, entre em contato com [rafael.vivian@ifc.edu.br](rafael.vivian@ifc.edu.br)")
    #st.markdown('<img src="ufrgs.png" alt="UFRGS" width="481" height="82">', unsafe_allow_html=True)
    st.image("ufrgs3.png")

def pagina_mapa():
    st.title("Mapa CSA App")
    st.write(f"Olá, professor(a) {st.session_state['nome']}!")
    st.write(f"Importante: os arquivos CSV devem estar padrodizados de acordo com as orientações neste link. Esse link também apresenta um exemplo de como o arquivo CSV deve ser preenchido. Você pode preencher os dados neste link e depois exportar o arquivo como CSV.") 
    
    arquivo_questionario = st.file_uploader(
        "Faça upload de um arquivo CSV [RESPOSTAS DO QUESTIONÁRIO]", 
        type=['csv']
    )

    if arquivo_questionario is not None:  
      st.write("Arquivo carregado com sucesso!")

    arquivo_aspectos = st.file_uploader(
        "Faça upload de um arquivo CSV [ASPECTOS SOCIAIS E AFETIVOS]", 
        type=['csv']
    )

    if arquivo_aspectos is not None:  
      st.write("Arquivo carregado com sucesso!")     

    if arquivo_questionario:        
      tipo = arquivo_questionario.name.split(".")[-1]
      if (tipo == 'csv'):
        df = read_csv(arquivo_questionario, index_col=0).transpose()
        #st.dataframe(df)
        with st.container():
            st.write("---")
            estudante_selecionado = st.selectbox("Selecione um estudante", df.columns, key=widget_key1)
            valores_estudante_selecionado = df[estudante_selecionado]
            st.line_chart(valores_estudante_selecionado)

    if arquivo_aspectos:        
      tipo = arquivo_aspectos.name.split(".")[-1]
      if (tipo == 'csv'):
        df = read_csv(arquivo_aspectos, index_col=0).transpose()
        #st.dataframe(df)
        with st.container():            
            estudante_selecionado = st.selectbox("Selecione um estudante", df.columns, key=widget_key2)

            valores_estudante_selecionado = df[estudante_selecionado]

            st.write(valores_estudante_selecionado)   

            tp_realizacao = df.iloc[1][estudante_selecionado]
            #st.write(tp_realizacao)

            tp_abertura = df.iloc[0][estudante_selecionado]
            #st.write(tp_abertura)

            as_interacao = df.iloc[5][estudante_selecionado]
            #st.write(as_interacao)

            aa_estado_animo = df.iloc[6][estudante_selecionado]            
            #st.write(aa_estado_animo)             

            aa_familia_afetiva = df.iloc[7][estudante_selecionado]
            #st.write(aa_familia_afetiva)
            
            aa_fatores_motivacionais = df.iloc[8][estudante_selecionado]

            #if aa_estado_animo != "indefinido":
               #estado_animo = extrai_estado_animo(aa_estado_animo)

            #else:
               #satisfeito = 0
               #animado = 0

            if aa_fatores_motivacionais != "indefinido":
               confianca = extrai_fator_motivacional(aa_fatores_motivacionais, "0")                                
               esforco = extrai_fator_motivacional(aa_fatores_motivacionais, "1")
               independencia = extrai_fator_motivacional(aa_fatores_motivacionais, "2")               
            else:
               confianca = 0.0
               esforco = 0.0
               independencia = 0.0            

            if aa_estado_animo == "indefinido":
               aa_estado_animo = 0.0

            if aa_familia_afetiva == "indefinido":
               aa_familia_afetiva = 0.0               

            if as_interacao != "indefinido":
               # eliminar linha abaixo
               #as_interacao = "colaboração + popularidade"
               as_interacao = extrai_aspecto_social(as_interacao)
            else:
               as_interacao = "indefinido"

            infere_resiliencia(confianca, esforco, aa_estado_animo, aa_familia_afetiva, tp_realizacao, tp_abertura, independencia, as_interacao)

            

def main():
    if "nome" not in st.session_state:
        pagina_inicio()
    else:
        pagina_mapa()

if __name__ == "__main__":
    main()
