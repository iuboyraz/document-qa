import streamlit as st
from openai import OpenAI
import pandas as pd
import PyPDF2
from io import StringIO

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt, .md, .csv, .xlsx, or .pdf)", 
        type=("txt", "md", "csv", "xlsx", "pdf")
    )

    # Process the uploaded file
    document = None
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1]
        if file_type in ["txt", "md"]:
            # Read text files
            document = uploaded_file.read().decode()
        elif file_type == "csv":
            # Read CSV files
            df = pd.read_csv(uploaded_file)
            document = df.to_string()
        elif file_type == "xlsx":
            # Read Excel files
            df = pd.read_excel(uploaded_file)
            document = df.to_string()
        elif file_type == "pdf":
            # Read PDF files
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            document = ""
            for page in pdf_reader.pages:
                document += page.extract_text()

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not document,
    )

    if document and question:

        # Process the uploaded file and question.
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
