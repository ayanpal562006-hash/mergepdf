import streamlit as st
from pypdf import PdfWriter
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="PDF Merger",
    page_icon="📄",
    layout="centered"
)

# Title
st.title("📄 PDF Merger")
st.write("Upload multiple PDF files and combine them into one PDF.")

# Upload PDF files
uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    st.subheader("Selected PDF Files")

    # Display uploaded files
    for i, file in enumerate(uploaded_files, start=1):
        st.write(f"{i}. {file.name}")

    # Merge button
    if st.button("🔗 Merge PDFs"):

        try:
            writer = PdfWriter()

            # Add each uploaded PDF
            for uploaded_file in uploaded_files:

                # Create temporary file
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(uploaded_file.getbuffer())
                    temp_path = temp_file.name

                # Append PDF
                writer.append(temp_path)

                # Delete temporary file
                os.remove(temp_path)

            # Create output PDF
            output_file = "combined.pdf"

            writer.write(output_file)
            writer.close()

            st.success("✅ PDF files combined successfully!")

            # Read combined PDF
            with open(output_file, "rb") as pdf:
                pdf_data = pdf.read()

            # Download button
            st.download_button(
                label="⬇️ Download Combined PDF",
                data=pdf_data,
                file_name="combined.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")

else:
    st.info("Please upload two or more PDF files.")