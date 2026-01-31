import streamlit as st
from utils.api import upload_pdfs_api, safe_message


def render_uploader():
    st.sidebar.header("Upload PDFs")

    
    st.sidebar.info(
        "🩺 **MediBot accepts medical PDFs only** "
        
    )

    uploaded_files = st.sidebar.file_uploader(
        "Upload multiple PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if st.sidebar.button("Upload to DB") and uploaded_files:
        try:
            response = upload_pdfs_api(uploaded_files)
        except Exception:
            st.sidebar.markdown(
                """
                <div style="
                    background-color:#1f2933;
                    color:white;
                    padding:12px;
                    border-radius:8px;
                    font-size:14px;
                ">
                ⚠️ Could not reach the server. Please make sure the backend is running.
                </div>
                """,
                unsafe_allow_html=True
            )
            return

        msg = safe_message(response)

        if response.status_code == 200:
            st.sidebar.success("✅ Uploaded successfully")

            st.session_state["uploaded_pdf_names"] = [f.name for f in uploaded_files]
            if st.session_state["uploaded_pdf_names"]:
                st.session_state["selected_pdf"] = st.session_state["uploaded_pdf_names"][0]

        elif response.status_code == 400:
            
            st.sidebar.markdown(
                """
                <div style="
                    background-color:#1f2933;
                    color:white;
                    padding:14px;
                    border-radius:10px;
                    font-size:14px;
                    line-height:1.6;
                ">
                🌿 <b>Sorry, this file wasn’t added</b><br><br>
                It looks like this PDF is not related to medical information.<br><br>
                MediBot can only work with <b>medical PDFs</b>, such as documents about
                symptoms, conditions, treatments, or healthcare guidelines.
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            
            st.sidebar.markdown(
                """
                <div style="
                    background-color:#1f2933;
                    color:white;
                    padding:14px;
                    border-radius:10px;
                    font-size:14px;
                    line-height:1.6;
                ">
                ⚠️ Sorry it is not a medical pdf. <br><br>
                Please upload only medical documents.
                </div>
                """,
                unsafe_allow_html=True
            )
