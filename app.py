import sys
sys.path.append('/home/ubuntu/loan_analysis_app/scripts')

import streamlit as st
from analyser import analyse
import os

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Commercial Application Analyser",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS styling
    page_bg_img = """
    <style>
    .stApp {
        background: linear-gradient(to top right, #65dfc9, #6cdbeb);
        color: #000000;
    }
    .stMarkdown h1 {
        text-align: center;
        font-weight: bold;
    }
    .stMarkdown h2 {
        text-align: center;
        font-weight: bold;
    }
    .css-1cpxqw2 p, .css-1cpxqw2 label {
        font-size: 18px;
    }
    .css-1cpxqw2 {
        font-family: "Arial", sans-serif;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Sidebar with instructions
    st.sidebar.title("Instructions")
    st.sidebar.markdown("""
    1. Upload the **Industrial License document(pdf/image)**.\n
    2. Upload the **Commercial Registration Documentdocument(pdf/image)**.\n
    2. Upload the **Loan Apllication Document(pdf/.docx)**.\n
    3. Click **Start Analysis** and wait for the results.\n
    4. Ensure the uploaded files are valid and readable.
    """)
    st.sidebar.markdown("**Contact:** placeholder@example.com")

    # Main title and headers
    st.markdown("<h1>Commercial Application Analyser</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h2>Upload the Required Documents</h2>", unsafe_allow_html=True)

    # Centered layout
    st.markdown(
        "<div style='display: flex; justify-content: center; align-items: center; flex-direction: column;'>",
        unsafe_allow_html=True,
    )

    # Upload buttons in rows
    uploaded_file1 = st.file_uploader("Upload Industrial License", type=["jpeg", "jpg", "png", "pdf"], key="file1")
    uploaded_file2 = st.file_uploader("Upload Commercial Registration", type=["jpeg", "jpg", "png", "pdf"], key="file2")
    uploaded_file3 = st.file_uploader("Upload Loan Application Form", type=["pdf", "docx"], key="file3")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Start Analysis", help="Click to process the uploaded files"):
        if uploaded_file1 and uploaded_file2:
            with st.spinner("Processing documents..."):
                # Create data directory if it doesn't exist
                if not os.path.exists("data"):
                    os.makedirs("data")

                # Save the uploaded files to the data directory
                # Using original filename provided by the user
                doc1_name = f"industrial_license.{uploaded_file1.name.split('.')[-1]}"
                doc2_name = f"commercial_registration.{uploaded_file2.name.split('.')[-1]}"
                doc3_name = f"loan_application_form.{uploaded_file3.name.split('.')[-1]}"

                # Save file 1
                with open(os.path.join("data", doc1_name), "wb") as f:
                    f.write(uploaded_file1.getbuffer())

                # Save file 2
                with open(os.path.join("data", doc2_name), "wb") as f:
                    f.write(uploaded_file2.getbuffer())

                # Save file 3
                with open(os.path.join("data", doc3_name), "wb") as f:
                    f.write(uploaded_file3.getbuffer())

                st.success("Documents uploaded successfully!")

                # Create a dictionary of the saved documents
                documents_info = {
                    "industrial_license": doc1_name,
                    "commercial_registration": doc2_name,
                    "loan_application": doc3_name
                }

                output = analyse(loan_app_name=documents_info["loan_application"],
                                 cr_name = documents_info["commercial_registration"],
                                 il_name=documents_info["industrial_license"]).get_results
                st.markdown("<h2>Processing Results</h2>", unsafe_allow_html=True)
                st.markdown(output)
        else:
            st.warning("Please upload all required documents before processing.")

if __name__ == "__main__":
    main()
