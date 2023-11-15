import streamlit as st
import base64
import gptable

if st.text_input("OpenAI API key", key="openai_api_key"):
    gptable.set_openai_api_key(st.session_state["openai_api_key"])

pdf_file = st.file_uploader("Upload your pdf here", type=["pdf"])

def displayPDF(file):
    base64_pdf = base64.b64encode(file.getvalue()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display =  f"""<embed class="pdfobject" type="application/pdf" title="Embedded PDF"
    src="data:application/pdf;base64,{base64_pdf}"
    style="overflow: auto; width: 100%; height: 100%;">"""
    # pdf_display = f"""<object data="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="100%" height="100%"></object>"""
    # pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="100%"></iframe>"""
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

if pdf_file:
    displayPDF(pdf_file)
    if st.button("Récupérer le csv simple"):
        with st.spinner("Calcul du csv par tabula..."):
            df_data = gptable.basic_pdf_to_df(pdf_file)
        st.session_state["df_data"] = df_data
if "df_data" in st.session_state:
    with st.expander("csv initial"):
        st.dataframe(st.session_state["df_data"])
    

    system_prompt_cols = st.text_area("Prompt pour la récupération des lignes et des colonnes")

    col1, col2 = st.columns(2)
    if col1.button("Récupérer lignes et colonnes"):
        with st.spinner("Appel à gpt-3.5 en cours..."):
            rows, cols = gptable.gpt_rows_and_cols(st.session_state["df_data"], system_prompt_cols)
        st.session_state["rows"] = rows
        st.session_state["cols"] = cols
    if col2.button("Lignes et colonnes manuelles"):
        st.session_state["rows"] = "[]"
        st.session_state["cols"] = "[]"
    if "rows" and "cols" in st.session_state:
        rows = st.text_area("Lignes", value=st.session_state["rows"])
        cols = st.text_area("Colonnes", value=st.session_state["cols"])

        system_prompt_values = st.text_area("Prompt pour la récupération des valeurs de lignes et de colonnes")

        if st.button("Récupérer les données"):
            with st.spinner("Appel à gpt-3.5 en cours..."):
                st.session_state['final_df'] = gptable.gpt_clean_df(st.session_state["df_data"], eval(rows), eval(cols), system_prompt_values)
        if "final_df" in st.session_state:
            st.dataframe(st.session_state["final_df"])
