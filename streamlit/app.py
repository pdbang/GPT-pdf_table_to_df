import streamlit as st
import base64
import gptable
import display_pdf as pdf
from pandas import DataFrame
from io import StringIO

st.title("PDF to table with LLM")
st.subheader("Utilisation example of gptable")

pdf_file = st.file_uploader("Upload your pdf here", type=["pdf"])

# def displayPDF(file):
#     base64_pdf = base64.b64encode(file.getvalue()).decode('utf-8')
#     # Embedding PDF in HTML
#     pdf_display =  f"""<embed class="pdfobject" 
#     type="application/pdf" 
#     title="Embedded PDF"
#     src="data:application/pdf;base64,{base64_pdf}"
#     style="overflow: auto; 
#     width: 100%; 
#     height: 100%;">"""
#     st.markdown(pdf_display, unsafe_allow_html=True)

st.button("As")
if pdf_file:
    # displayPDF(pdf_file)
    if "img_path" not in st.session_state or "pdf_name" not in st.session_state or pdf_file.name != st.session_state["pdf_name"]:
        st.session_state["img_path"] = pdf.pdf_to_img(pdf_file)
        st.session_state["pdf_name"] = pdf_file.name
    pdf.display_img(st.session_state["img_path"])
    if st.button("Récupérer le csv simple"):
        with st.spinner("Calcul du csv par tabula..."):
            df_data = gptable.basic_pdf_to_df(pdf_file)
        st.session_state["df_data"] = df_data
if "df_data" in st.session_state:
    with st.expander("csv initial"):
        st.dataframe(st.session_state["df_data"])
    
    if st.text_input("OpenAI API key", key="openai_api_key"):
        gptable.set_openai_api_key(st.session_state["openai_api_key"])

    system_prompt_cols = st.text_area("Prompt pour la récupération des lignes et des colonnes")

    col1, col2 = st.columns(2)
    if col2.button("Récupérer lignes et colonnes"):
        with st.spinner("Appel à gpt-3.5 en cours..."):
            rows, cols = gptable.gpt_rows_and_cols(st.session_state["df_data"], system_prompt_cols)
        st.session_state["rows"] = DataFrame(rows, columns=["Rows"])
        st.session_state["cols"] = DataFrame(cols, columns=["Columns"])
    if col1.button("Lignes et colonnes manuelles"):
        st.session_state["rows"] = DataFrame(columns=["Rows"])
        st.session_state["cols"] = DataFrame(columns=["Columns"])
    if "rows" and "cols" in st.session_state:
        rows = col1.data_editor(st.session_state["rows"], num_rows="dynamic", height=200)
        cols = col2.data_editor(st.session_state["cols"], num_rows="dynamic", height=200)

        system_prompt_values = st.text_area("Prompt pour la récupération des valeurs de lignes et de colonnes")

        if st.button("Récupérer les données"):
            with st.spinner("Appel à gpt-3.5 en cours..."):
                st.session_state['final_df'] = gptable.gpt_clean_df(st.session_state["df_data"], rows["Rows"].tolist(), cols["Columns"].tolist(), system_prompt_values)
        if "final_df" in st.session_state:
            st.dataframe(st.session_state["final_df"])
            if st.button("Export to csv"):
                csv_data = StringIO()
                st.session_state["final_df"].to_csv(csv_data)
                st.download_button("Download csv", csv_data.getvalue(), f"{pdf_file.name.split('.')[0]}_clean.csv")
