import requests
from bs4 import BeautifulSoup
import spacy
from gensim.models.phrases import Phrases, Phraser
import tldextract
from rake_nltk import Rake

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Fetch the webpage content
def get_webpage_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.text
    else:
        print(response.status_code)
        print("Error fetching the webpage content.")
        return None

# Function to get the base domain from a URL
def get_base_domain(url):
    extracted = tldextract.extract(url)
    return "{}.{}".format(extracted.domain, extracted.suffix)

# Extract meaningful phrases using Gensim
def get_phrases(tokens):
    # Build the phrase model
    phrases = Phrases(tokens, min_count=1, threshold=1)
    phraser = Phraser(phrases)
    all_phrases = list(phraser[tokens])
    # Flatten the list of lists and filter '_'
    return list(set(phrase for phrase_list in all_phrases for phrase in phrase_list if '_' in phrase))

# Use Rake for keyword extraction
def get_rake_keywords(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()

# Main function to extract keywords and identify website
def main():
    # The URL of the webpage for which to extract keywords
    url = 'https://www.tesco.ie/'
    base_domain = get_base_domain(url)
    print(f"Website Domain: {base_domain}")

    html_content = get_webpage_content(url)

    if html_content:
        # Using BeautifulSoup to parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract meaningful text from the soup object - like <p>, <h1>, <h2>... tags
        text = ' '.join(t.get_text() for t in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li']))
        # # Process the text using spaCy
        # doc = nlp(text)
        # # Filter tokens that are not stop words or punctuations and are either noun or adjective
        # tokens = [[token.lemma_.lower() for token in sent if not token.is_stop and not token.is_punct and token.pos_ in ('NOUN', 'ADJ')] for sent in doc.sents]
        # # Extract meaningful phrases with Gensim
        # meaningful_phrases = get_phrases(tokens)
        # print("\nExtracted Meaningful Phrases:")
        # print(meaningful_phrases)

        # Extract keywords with Rake
        rake_keywords = get_rake_keywords(text)
        print("\nRanking of RAKE Keywords:")
        rake_keywords = set(rake_keywords)
        for keyword in rake_keywords:
            print(keyword)

if __name__ == "__main__":
    main()