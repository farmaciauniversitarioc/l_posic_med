import streamlit as st
import pandas as pd
from processamento import processar_r84
from io import BytesIO

st.set_page_config(page_title="Relatório R84", layout="wide")

st.title("Relatório de Posição de Medicamentos")
st.write("Envie um arquivo R84 (.xls) para gerar o relatório consolidado.")

arquivo_enviado = st.file_uploader(
    "Selecione o arquivo R84",
    type=["xls"]
)

if arquivo_enviado is not None:

    with st.spinner("Processando arquivo..."):
        df_final = processar_r84(arquivo_enviado)

    if df_final.empty:
        st.warning("Nenhum registro encontrado no arquivo.")
    else:

        st.success("Arquivo processado com sucesso.")

        st.subheader("Filtros")

        col1, col2, col3 = st.columns(3)

        with col1:
            estabelecimentos = sorted(df_final["estabelecimento_saude"].unique())
            filtro_estabelecimento = st.multiselect(
                "Estabelecimento de saúde",
                estabelecimentos
            )

        with col2:
            catmats = sorted(df_final["catmat"].unique())
            filtro_catmat = st.multiselect(
                "CATMAT",
                catmats
            )

        with col3:
            filtro_medicamento = st.text_input(
                "Descrição do medicamento"
            )

        df_filtrado = df_final.copy()

        if filtro_estabelecimento:
            df_filtrado = df_filtrado[
                df_filtrado["estabelecimento_saude"].isin(filtro_estabelecimento)
            ]

        if filtro_catmat:
            df_filtrado = df_filtrado[
                df_filtrado["catmat"].isin(filtro_catmat)
            ]

        if filtro_medicamento:
            df_filtrado = df_filtrado[
                df_filtrado["medicamento"].str.contains(
                    filtro_medicamento,
                    case=False,
                    na=False
                )
            ]

        st.subheader("Relatório Processado")

        st.dataframe(
		df_filtrado.drop(columns=["catmat"],
		use_container_width=True
    	)


        st.write(f"Total de registros exibidos: {len(df_filtrado)}")

        # Preparar download do Excel

        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_filtrado.to_excel(writer, index=False)

        st.download_button(
            label="Baixar relatório em Excel",
            data=output.getvalue(),
            file_name="relatorio_processado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )
