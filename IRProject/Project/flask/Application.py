from flask import Flask, request, jsonify, render_template
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.metrics import edit_distance


# Download NLTK data for word tokenization (punkt) and WordNet
nltk.download('punkt')
nltk.download('wordnet')

# Create a Flask web application
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def index():
    # Render the 'template.html' template located in the 'templates' folder
    return render_template('template.html')

# This code initializes the Flask application and sets up a route for the homepage.
# When a user accesses the homepage, the 'template.html' template will be rendered and displayed.

@app.route('/query', methods=['POST'])
def process_query():
    data = request.json

    # Validate the request
    if 'query' not in data or 'k' not in data:
        return jsonify({'The request is invalid because it is missing either the "query" or the "k" parameter.'}), 400

    query = data['query']
    k = data['k']

    # Spelling correction/suggestion
    spell_checked_query = improve_word_spelling(query)

    # Query expansion
    expanded_query = expand_spell_checked_query(spell_checked_query)

    # Search the dataset for relevant results
    results = retrieve_search_results(expanded_query, k)

    return jsonify({'results': results, 'corrected_query': spell_checked_query, 'expanded_query': expanded_query})

def retrieve_search_results(query, k):
    # Tokenize the query into words
    words = word_tokenize(query)
    
    # Initialize an empty list to store the results
    results = []
    
    # Iterate over each word in the query
    for word in words:
        # Get the synsets (sets of synonyms) for the word
        synsets = wordnet.synsets(word)
        
        # Iterate over each synset
        for synset in synsets:
            # Iterate over each lemma in the synset
            for lemma in synset.lemmas():
                # Append the result to the results list
                results.append({
                    'id': len(results) + 1,  # Generate a unique ID for the result
                    'word': lemma.name(),     # Get the name of the lemma
                    'definition': synset.definition()  # Get the definition of the synset
                })
                
                # Check if the number of results is greater than or equal to k
                if len(results) >= int(k):
                    break  # Exit the innermost loop
                
            if len(results) >= int(k):
                break  # Exit the middle loop
        
        if len(results) >= int(k):
            break  # Exit the outermost loop
    
    # Return the results
    return results


def improve_word_spelling(query):
    # Tokenize the query into words
    tokens = word_tokenize(query)
    
    # Correct each word in the query
    corrected_tokens = [correct_word(token) for token in tokens]
    
    # Join the corrected tokens back into a single string
    return ' '.join(corrected_tokens)

def correct_word(word):
    # Get the possible meanings (synsets) of the word
    candidates = wordnet.synsets(word)
    
    # If there are no meanings, return the original word
    if not candidates:
        return word
    
    # Initialize a set to store candidate words
    candidate_words = set()
    
    # Iterate over each synset
    for candidate in candidates:
        # Add the lemma names (synonym words) to the set
        candidate_words.update(candidate.lemma_names())
    
    # Choose the candidate word with the smallest edit distance from the original word
    return max(candidate_words, key=lambda x: edit_distance(word, x))

def expand_spell_checked_query(query):
    # Tokenize the query into words
    tokens = word_tokenize(query)
    
    # Expand each word in the query
    expanded_tokens = [expand_word(token) for token in tokens]
    
    # Join the expanded tokens back into a single string
    return ' '.join(expanded_tokens)

def expand_word(word):
    # Initialize a set to store synonyms
    synonyms = set()
    
    # Get the synsets (sets of synonyms) for the word
    for syn in wordnet.synsets(word):
        # Iterate over each lemma in the synset
        for lemma in syn.lemmas():
            # Add the lemma name to the set of synonyms
            synonyms.add(lemma.name())
    
    # Join the synonyms into a single string
    return ' '.join(synonyms)


if __name__ == '__main__':
    # Run the Flask application in debug mode
    # Debug mode allows for easier debugging by providing detailed error messages
    # and automatically restarting the server when code changes are detected
    app.run(debug=True)

