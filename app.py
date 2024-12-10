import streamlit as st
from scripts.analyser import analyse
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
    1. Upload your *Industrial License* document.\n
    2. Upload your *Commercial Registration* document.\n
    3. Click **Process Documents** and wait for the results.\n
    4. Ensure the uploaded files are valid and readable.
    """)
    st.sidebar.markdown("**Contact:** support@example.com")

    # Main title and headers
    st.markdown("<h1>Commercial Application Analyser</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h2>Upload the Required Documents</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        uploaded_file1 = st.file_uploader("Upload Industrial License", type=["pdf", "docx", "jpeg", "jpg", "png"], key="file1")
    with col2:
        uploaded_file2 = st.file_uploader("Upload Commercial Registration", type=["pdf", "docx"], key="file2")

    if st.button("Analyse Documents", help="Click to process the uploaded files"):
        if uploaded_file1 and uploaded_file2:
            with st.spinner("Processing documents..."):
                # Create data directory if it doesn't exist
                if not os.path.exists("data"):
                    os.makedirs("data")

                # Save the uploaded files to the data directory
                # Using original filename provided by the user
                doc1_name = f"industrial_license.{uploaded_file1.name.split(".")[-1]}"
                doc2_name = f"commercial_registration_form.{uploaded_file2.name.split(".")[-1]}"
                
                # Save file 1
                with open(os.path.join("data", doc1_name), "wb") as f:
                    f.write(uploaded_file1.getbuffer())

                # Save file 2
                with open(os.path.join("data", doc2_name), "wb") as f:
                    f.write(uploaded_file2.getbuffer())

                st.success("Documents uploaded successfully!")

                # Create a dictionary of the saved documents
                documents_info = {
                    "Industrial_License": doc1_name,
                    "Commercial_Registration": doc2_name
                }

                # Example processing result
                output = analyse(cr_name=documents_info["Commercial_Registration"],
                                     il_name=documents_info["Industrial_License"]).get_results
                result = output

                st.markdown("<h2>Processing Results</h2>", unsafe_allow_html=True)
                st.markdown(result)
        else:
            st.warning("Please upload both documents before processing.")

if __name__ == "__main__":
    main()