import requests
from bs4 import BeautifulSoup
from googlesearch import search
from nltk.tokenize import sent_tokenize
from urllib.parse import urlparse, urljoin


def get_website_sentences(url):
    """
    Fetch the text content of a website and tokenize it into sentences.

    Args:
        url (str): The URL of the website.

    Returns:
        list: A list of sentences extracted from the website text.
            Returns None if there is an HTTP error, a general request exception, or crawling is not allowed.
    """
    try:
        # Parse the base URL
        base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

        # Check if the website allows crawling based on the robots.txt file
        robots_url = urljoin(base_url, "/robots.txt")
        response = requests.get(robots_url)
        if response.status_code == 200:
            robots_content = response.text
            if (
                "User-agent: *" in robots_content
                and "Disallow: /" not in robots_content
            ):
                # Website allows crawling, proceed with fetching the content
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                text = soup.get_text(separator="\n")
                return sent_tokenize(text)
            else:
                print(
                    f"Crawling not allowed for {base_url}. Please check the website's robots.txt file."
                )
                return None
        else:
            print(f"Unable to fetch {robots_url}. Proceeding with scraping.")
            # Website robots.txt not found, proceed with scraping
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text(separator="\n")
            return sent_tokenize(text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_top_links(search_query):
    """
    Search for the top 5 relevant links for a given search query.

    Args:
        search_query (str): The search query to perform.

    Returns:
        list: A list of the top 5 relevant links.
    """
    return list(search(search_query, num_results=5))


def search_phrase(phrase: str, sentences):
    """
    Check if a given phrase is present in any of the provided sentences.

    Args:
        phrase (str): The phrase to search for.
        sentences (list): A list of sentences to search in.

    Returns:
        bool: True if the phrase is found in any of the sentences, False otherwise.
    """
    return any(phrase in sentence for sentence in sentences)
