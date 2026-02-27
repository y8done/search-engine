# import nltk
# # nltk.download('punkt_tab') 
# # nltk.download('stopwords') 
# # nltk.download('wordnet')

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

url_queue = []
visited_urls = set()

headers = {
    'User-Agent': 'MySearchEngineProject/1.0 (your_email@example.com)'
}

def crawl(base_url, start_url, max_pages=500):

    url_queue.append(start_url)
    pages_crawled = 0
    if os.path.isdir('dataset'):
      print("Folder exists")
    else:
      os.makedirs("dataset",exist_ok=True)
    while url_queue and pages_crawled < max_pages:
        current_url = url_queue.pop(0)

        if current_url in visited_urls:
            continue

        try:
            print(f"[{pages_crawled + 1}] Crawling : {current_url}")

            response = requests.get(current_url, headers=headers, timeout=5)
            visited_urls.add(current_url)
            pages_crawled += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {current_url}: {e}")
            continue
        

        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('div', id="mw-content-text")
        h1_tag = soup.find('h1')
        if h1_tag:
          heading=h1_tag.text
        else:
          heading="unknown_page"
        safe_heading = heading.replace('/','-').replace(':','').replace('?','')

        if main_content:
            links = main_content.find_all('a')
            paras = main_content.find_all('p')    
        else:
            links = []
            paras=[]
        if paras:
          try:
            filepath = os.path.join("dataset/",f"{safe_heading}.txt")
            with open(filepath,'w',encoding='utf-8') as file:
              file.write(current_url + "\n")
              for p in paras:
                file.write(p.text.strip() + "\n")
          except IOError as e:
            print(f"Error occurred : {e}")
        for link in links:
            href = link.get('href')
            if not href or href.startswith('#'):
                continue
            full_url = urljoin(current_url, href)

            if full_url not in visited_urls and full_url not in url_queue:
                if "en.wikipedia.org/wiki/" in full_url:
                    url_queue.append(full_url)

if __name__ == "__main__":
    crawl("https://en.wikipedia.org/wiki/", "https://en.wikipedia.org/wiki/Programming_language")
    print("Crawl complete!")