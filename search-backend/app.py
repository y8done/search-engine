import json
import math
import string
from collections import defaultdict
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from flask import Flask, request, jsonify
from flask_cors import CORS
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def tokenize_and_clean(text):
    text = text.lower()
    tokens = word_tokenize(text)
    clean_tokens = []
    for word in tokens:
        if word not in stop_words and word not in string.punctuation:
            root_word = lemmatizer.lemmatize(word, pos='v')
            clean_tokens.append(root_word)
    return clean_tokens

print("Loading search engine database...")
with open("inverted_index.json", "r") as f:
    inverted_index = json.load(f)

with open("doc_lengths.json", "r") as f:
    doc_lengths = json.load(f)

TOTAL_DOCS = len(doc_lengths)
print(f"Engine ready! {TOTAL_DOCS} documents loaded.")

def search(query):
  tokens = tokenize_and_clean(query)
  if not tokens:
        return []
  scores = defaultdict(float)

  for token in tokens:
    if token not in inverted_index:
      continue
    
    df = len(inverted_index[token])
    idf = math.log( TOTAL_DOCS / df)

    for url, term_count in inverted_index[token].items():

      tf = term_count / doc_lengths[url]

      scores[url] += (tf * idf)
  ranked_urls = sorted(scores.items(), key=lambda item: item[1], reverse=True)

  return ranked_urls

app = Flask(__name__)
CORS(app)
@app.route('/search', methods=['GET'])
def api_search():
    user_query = request.args.get('query', '')

    if not user_query:
        return jsonify({"error": "No query provided", "results": []}), 400

    ranked_results = search(user_query)

    formatted_results = []
    for url, score in ranked_results[:10]:
        formatted_results.append({
            "url": url,
            "score": round(score, 4)
        })
        

    return jsonify({"query": user_query, "results": formatted_results})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
















# while True:
#     query = input("\nSearch Wikipedia (or 'exit' to quit): ")
#     if query.lower() == 'exit':
#         break
        
#     results = search(query)
    
#     if not results:
#         print("No matches found.")
#     else:
#         print(f"\nTop results for '{query}':")
#         # Print top 5 results
#         for i, (url, score) in enumerate(results[:5], 1):
#             print(f"  {i}. {url} (Score: {score:.4f})")