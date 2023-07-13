import streamlit as st
import pandas as pd

from doc_functions import read_document, calculate_plagiarism_percentage
from search import get_top_links, get_website_sentences, search_phrase

st.title("Plagiarism Detector*📑")


file = st.file_uploader("Upload a Word or PDF file", type=["docx", "pdf"])

if file is not None:
    if (
        file.type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        st.success("Word file has been uploaded!")
        # Process the Word file here
    elif file.type == "application/pdf":
        st.success("PDF file has been uploaded!")
        # Process the PDF file here
    else:
        st.error("The file type is incompatible. A Word or PDF document should be uploaded.")


if submit_button := st.button("Submit"):
    if file is None:
        st.error("No file has been selected. Please upload a file before submitting.")
    else:
        plagiarized = []
        doc_lines = read_document(file)
        progress_bar = st.progress(
            0
        )  # Create a progress bar with an initial value of 0

        for i, line in enumerate(doc_lines):
            top_links = get_top_links(line)
            for link in top_links:
                website_text = get_website_sentences(link)
                if website_text is not None and search_phrase(line, website_text):
                    plagiarized.append([line, link])

            progress = (i + 1) / len(doc_lines)  # Calculate the progress as a fraction
            progress_bar.progress(progress)  # Update the progress bar

        plagiarism = calculate_plagiarism_percentage(len(doc_lines), len(plagiarized))

        # Display the plagiarism result and other relevant information
        st.write("Plagiarism Percentage:", plagiarism, "%")
        st.write("Total Lines:", len(doc_lines))
        st.write("Plagiarized Lines:", len(plagiarized))

        if plagiarized:
            st.write("Plagiarized Text:")
            df = pd.DataFrame(plagiarized, columns=["Line", "Link"])
            st.table(df)
