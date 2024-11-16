import json
import os

from dotenv import load_dotenv
from llama_hub.confluence import ConfluenceReader

from utils import (get_confluence_credentials, parse_markdown_to_dict, remove_html_tags_from_json,
                   save_documents_in_json_file)

load_dotenv()
data_folder = os.getenv("DATA_FOLDER")


def load_data_from_confluence():
    print("Grab a coffee ☕︎ This may take a while!")
    loader = ConfluenceReader(base_url=creds["base_url"], cloud=False)
    documents = loader.load_data(
            page_ids=creds["page_ids"], include_children=True, include_attachments=False
            )

    return documents


def extract_content_and_metadata(document):
    base_url = document.metadata["url"]
    markdown_content = document.text
    sections = parse_markdown_to_dict(
            markdown_content, base_url, document.metadata["title"]
            )
    return sections


def process_documents(documents):
    all_processed_docuemnts = []
    for doc in documents:
        processed_docuemnt = extract_content_and_metadata(doc)
        all_processed_docuemnts.extend(processed_docuemnt)

    return all_processed_docuemnts


if __name__ == "__main__":
    # Check if the folder exists
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)  # Create the folder if it doesn't exist

    document_name_raw = os.path.join(data_folder, "confluence_data_raw.json")
    document_name_processed = os.path.join(data_folder, "confluence_data_processed_sections_split.json")
    document_name_processed_no_html_tags = os.path.join(data_folder,
                                                        "confluence_data_processed_sections_split_no_html_tags.json")

    creds = get_confluence_credentials()
    confluence_data = load_data_from_confluence()
    # JSON Conversion of raw data in order to save it
    confluence_data_json = json.dumps(
            confluence_data, default=lambda x: x.__dict__, indent=4, ensure_ascii=False
            )
    save_documents_in_json_file(confluence_data_json, document_name_raw)

    processed_docuemnts = process_documents(confluence_data)
    save_documents_in_json_file(processed_docuemnts, document_name_processed)

    cleaned_data = remove_html_tags_from_json(document_name_processed)
    save_documents_in_json_file(cleaned_data, document_name_processed_no_html_tags)