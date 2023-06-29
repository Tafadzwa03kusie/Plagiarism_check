import requests
import os
import docx

file_path = r"C:\Users\hp\Desktop\DATA SCIENCE\ADS\Plagiarism checker website\Samples\Reading.docx"

def upload_file(file_path):

    """Opening and reading the contents of the file"""
    try:

        with open(file_path, "rb") as file:
            file_content= file.read()

        url = "https://example.com/upload"

        headers = {
            "Content-Type": "application/octet-stream",
            "Content-Disposition": f"attachment; filename={file_path}"
        }
        response = requests.post(url, headers=headers, data=file_content)

        return response.text
    except Exception as e:
        # Log the error
        print(f"Error: {e})")
        return ""


"""Uploading the file to a web application, and returning similar content found on the internet"""
def get_similar_content(file_path):

    try:
        # Does the file exist
        with open(file_path,"rb") as f:
            pass
        # Uploading it to the web application
        url = "https://example.com/upload"
        files = {"file": open(file_path, "rb")}
        response = requests.post(url, files=files)

        # Get the similar content from the response
        similar_content = response.text

        return similar_content
    except FileNotFoundError:
        # Logging error
        print(f"Error: File {file_path} not found")
        return ""
    except Exception as e:
        # Logging error
        print(f"Error: {e}")
        return ""


"""Extracting random phrases from the contents of an uploaded file"""
from flask import Flask, request

app = Flask(__name__)

@app.route('/extract_phrases', methods=['POST'])
def extract_phrases():

    try:
        # Was the file uploaded
        if 'file' not in request.files:
            raise ValueError("No file was uploaded")

        # Reading the file contents
        file = request.files['file']
        contents = file.read().decode('utf-8')

        # Extracting some phrases from the contents
        phrases = contents.split('.')
        random_phrase = random.choice(phrases)

        # Return a random phrase
        return random_phrase
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return "An error occurred while processing your request"


import random


def extract_random_phrases(url):
    try:
        # Making a GET request to the URL
        response = requests.get(url)

        # Parsing the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting all text from the document
        text = soup.get_text()

        # Splitting the text into phrases
        phrases = text.split('.')

        # Selecting 5 random phrases
        random_phrases = random.sample(phrases, 5)

        return random_phrases
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return []


def run_google_search(phrase):
    try:
        # Constructing the Google search URL
        search_url = f"https://www.google.com/search?q={phrase}"

        # Making a GET request to the search URL
        response = requests.get(search_url)

        # Parsing the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting the URL of the first search result
        search_result = soup.find('div', class_='BNeawe UPmit AP7Wnd').get_text()

        return search_result
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return ""


def build_web_application(url):
    try:
        # Extracting random phrases from the document
        phrases = extract_random_phrases(url)

        # Running a Google search against each phrase and printing the results
        for phrase in phrases:
            search_result = run_google_search(phrase)
            print(f"Search result for '{phrase}': {search_result}")
    except Exception as e:
        # Logging the error
        print(f"Error: {e}")

from bs4 import BeautifulSoup


def scrape_google_results(phrases):
    try:
        # Checking if phrases is a list
        if not isinstance(phrases, list):
            raise TypeError("Input must be a list of phrases")

        # Creating an empty dictionary to store the results
        results = {}

        # Looping through each phrase in the list
        for phrase in phrases:
            # Creating an empty list for storing the results for this phrase
            phrase_results = []

            # Searching on Google for the phrase
            url = f"https://www.google.com/search?q={phrase}"
            response = requests.get(url)

            # Parsing the HTML content of the response
            soup = BeautifulSoup(response.content, "html.parser")

            # Finding the top five search results
            search_results = soup.find_all("div", class_="g")[:5]

            # Looping through each search result
            for result in search_results:
                # Finding the main text of the page
                main_text = result.find("div", class_="s").get_text()

                # Cleaning the main text by removing any unwanted characters
                main_text = main_text.replace("\n", " ").strip()

                # Adding the cleaned main text to the list of results for this phrase
                phrase_results.append(main_text)

            # Adding the list of results for this phrase to the dictionary
            results[phrase] = phrase_results

        # Returning the dictionary of results
        return results
    except Exception as e:
        # Logging the error
        print(f"Error: {e}")
        return {}



import requests

# Comparing the contents and return the result
def compare_file_to_webpage(file_path, url):
    try:

        with open(file_path, 'r') as f:
            file_contents = f.read()


        response = requests.get(url)
        webpage_contents = response.text


        return file_contents == webpage_contents
    except Exception as e:

        print(f"Error: {e}")
        return False



