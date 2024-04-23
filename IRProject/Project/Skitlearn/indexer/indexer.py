import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Paths
DATA_DIR = "../data"
DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
INDEX_DIR = "."
INDEX_FILE = os.path.join(INDEX_DIR, "inverted_index.pickle")
COSINE_SIM_FILE = os.path.join(INDEX_DIR, "cosine_similarity.pickle")

# Sample documents
documents = []
for filename in os.listdir(DOCUMENTS_DIR):
    with open(os.path.join(DOCUMENTS_DIR, filename), "r") as file:
        documents.append(file.read())

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# Create inverted index
terms = vectorizer.get_feature_names_out()
inverted_index = {term: {} for term in terms}
for i, term in enumerate(terms):
    for j in range(len(documents)):
        if X[j, i] > 0:
            inverted_index[term][j] = X[j, i]

# Compute cosine similarity
cosine_sim = cosine_similarity(X, X)

# Save inverted index and cosine similarity to pickle files
with open(INDEX_FILE, "wb") as file:
    pickle.dump(inverted_index, file)

with open(COSINE_SIM_FILE, "wb") as file:
    pickle.dump(cosine_sim, file)

# Load inverted index and cosine similarity from pickle files
with open(INDEX_FILE, "rb") as file:
    loaded_inverted_index = pickle.load(file)

with open(COSINE_SIM_FILE, "rb") as file:
    loaded_cosine_sim = pickle.load(file)

# Example usage
query = "this is the second document"
query_vector = vectorizer.transform([query])
query_cosine_sim = cosine_similarity(query_vector, X)[0]

print("Inverted Index:")
for term, postings in loaded_inverted_index.items():
    print(term, "->", postings)

print("\nCosine Similarity Matrix:")
print(loaded_cosine_sim)

print("\nCosine Similarity with Query:")
print(query_cosine_sim)
