import getpass
import json
import logging
import os
import re

import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


def get_confluence_credentials():
    os.environ["CONFLUENCE_URL"] = os.getenv("CONFLUENCE_URL")
    os.environ["CONFLUENCE_PAGE_ID"] = os.getenv("CONFLUENCE_PAGE_ID")
    os.environ["CONFLUENCE_USERNAME"] = (os.getenv("CONFLUENCE_USERNAME") or getpass.getuser())
    os.environ["CONFLUENCE_PASSWORD"] = (os.getenv("CONFLUENCE_PASSWORD") or getpass.getpass())

    return {
        "username": os.environ["CONFLUENCE_USERNAME"],
        "base_url": os.environ["CONFLUENCE_URL"],
        "password": os.environ["CONFLUENCE_PASSWORD"],
        "page_ids": [os.environ["CONFLUENCE_PAGE_ID"]],
        }


def parse_markdown_to_dict(markdown_content, base_url, title):
    # Pre-process multi-line headers
    lines = markdown_content.split('\n')
    joined_lines = []
    header_started = False
    current_header = ""

    # Iterate through lines to handle multi-line headers
    for line in lines:
        # Check if the line starts with a header marker (# symbols)
        if re.match(r'^#+\s', line):
            # If a header was previously being processed, add it to joined lines
            if header_started:
                joined_lines.append(current_header)
            # Start a new header
            header_started = True
            current_header = line
        # If we're in a multi-line header and the line is not empty
        elif header_started and line.strip():
            # Append the line to the current header (with a space)
            current_header += " " + line.strip()
        else:
            # If a header was being processed, finalize it
            if header_started:
                joined_lines.append(current_header)
                header_started = False
            # Add the current line
            joined_lines.append(line)

    # Add the last header if it was being processed
    if header_started:
        joined_lines.append(current_header)

    # Rejoin the lines into a single markdown string
    markdown_content = '\n'.join(joined_lines)

    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content)
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Initialize variables to track sections
    sections = []
    current_section = None
    current_level = 0

    # Initialize variables to track sections
    for element in soup:
        # Check if the element is a header (h1, h2)
        if element.name in ["h1", "h2"]:
            header_level = int(element.name[1])

            """ If we were processing a previous section and the new header 
             is at the same or higher level, finalize the previous section """
            if current_section and header_level <= current_level:
                sections.append(current_section)
                current_section = None

            # Create a new section
            current_section = {
                "title": element.get_text(),
                "content": "",
                "link": f"{base_url}#{title}-{element.get_text()}".replace(" ", ""),
                # Parse the source to the information for RAG transparency
                }
            # Update the current header level
            current_level = header_level

        # If we're currently processing a section
        elif current_section:
            """Add content to the current section
            Only add content if it's at the same or one level below the header """
            if (current_level + 1 >= int(element.name[1]) if element.name in ["h1", "h2", "h3"] else current_level):
                current_section["content"] += str(element)

    # Add the last section if it exists
    if current_section:
        sections.append(current_section)

    return sections


def save_documents_in_json_file(docuemnts, document_name="data.json"):
    with open(document_name, "w", encoding="utf-8") as json_file:
        json.dump(docuemnts, json_file, indent=4, ensure_ascii=False)


def load_json_file(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        return json.load(file)


def remove_html_tags(text):
    # Use BeautifulSoup to remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text()
    # Remove newline characters
    clean_text = clean_text.replace('\n', ' ')
    return clean_text


def clean_json(data):
    """
    Recursively clean a JSON-like data structure by removing HTML tags from string values.
    """
    if isinstance(data, dict):
        return {k: clean_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_json(item) for item in data]
    elif isinstance(data, str):
        return remove_html_tags(data)
    else:
        return data


def remove_html_tags_from_json(file_name):
    # Load the JSON file
    json_data = load_json_file(file_name)

    # Clean the JSON data
    cleaned_data = clean_json(json_data)

    return cleaned_data