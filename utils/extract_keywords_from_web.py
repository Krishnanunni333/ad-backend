from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from openai import OpenAI
from dotenv import load_dotenv
import os
import tldextract
import requests
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# Download NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')

def get_base_domain(url: str) -> str:
    extracted = tldextract.extract(url)
    return "{}.{}".format(extracted.domain, extracted.suffix)


# Function to get the text content from a website
def get_website_text(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text

# Function to extract keywords from text
def extract_keywords(text: str) -> list[str]:
    # Tokenize the text
    words = word_tokenize(text)

    # Remove stopwords (common words that usually don't contribute much to the meaning)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    # Calculate word frequencies
    freq_dist = FreqDist(filtered_words)

    common_words = list()
    for word in freq_dist.most_common(20):
        common_words.append(word)
    # print(common_words)
    return common_words


def get_keywords_using_gpt(words: list[str], website_url: str) -> set[str]:
    # Fetch website content (you can use requests or any other method)
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": 'You should behave like an advanced keyword filter.\
                           Analyze the keywords that is passed and output the keywords that is most relevant and context based.'},
                            {"role": "user", "content": f'Extract 5 keywords from the given list of keywords. I scraped these keywords from the website.\
                              The URL of the website is {website_url}.\
                            Please consider the context of the website.\
                            Output the country of the website with keywords.\
                            Include the audience of the website in keywords.\
                            Current keywords are : {words}. Only return the relevant keywords as comma seperated values.\
                            Do not return any other text.'},
                ])

        # Extract generated keywords from the response
        result = set([
                item.strip()
                for item in response.choices[0].message.content.split(",")
                if item
            ])
        # print(result)
    except Exception as e:
        print(f"Exception occured!\n {e}")
        return

    return result

def get_website_content(url: str) -> str:
    # Implement the logic to fetch content from the website (e.g., using requests)
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website content: {e}")
        return ""

def get_keywords(url: str) -> list[str]:
    website_text = get_website_content(url)
    words = extract_keywords(website_text)
    keywords = list(get_keywords_using_gpt(words, url))
    keywords.append(get_base_domain(url))
    return keywords

