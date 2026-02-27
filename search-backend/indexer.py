import os
import json
import string
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


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



file_names = os.listdir("dataset")
print(file_names)
inverted_index = defaultdict(lambda: defaultdict(int))
doc_lengths = defaultdict(int)


for f in file_names:
  if not f.endswith(".txt"):
      continue
  try:
    filepath = os.path.join("dataset/",f)

    with open(filepath,'r',encoding='utf-8') as file:
      source_url = file.readline().strip()
      for line in file:
        tokens = tokenize_and_clean(line)

        for token in tokens:
          if token not in inverted_index:
            inverted_index[token] = {}
          if source_url not in inverted_index[token]:
            inverted_index[token][source_url] = 0
          inverted_index[token][source_url] += 1 

          doc_lengths[source_url] += 1

  except IOError as e:
    print(f"Error occurred {e}")
print(inverted_index)

print("Saving brain to disk...")
with open("inverted_index.json", "w") as f:
    json.dump(inverted_index, f)

with open("doc_lengths.json", "w") as f:
    json.dump(doc_lengths, f)

print("Indexing complete! You can now run app.py")
