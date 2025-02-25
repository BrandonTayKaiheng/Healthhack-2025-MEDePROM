# Converts corpus entries (JSON) into vector embeddings
# Pretrained sentence transformer from: https://sbert.net/docs/sentence_transformer/pretrained_models.html

from sentence_transformers import SentenceTransformer 
import json

# Load json corpus
corpus_path = "" # Insert path here
with open(corpus_path, "r", encoding="utf-8") as f:
    corpus = json.load(f)

# Load pretrained model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') # Can try others

# Prepare text data for embedding (combine question and options)
texts = [
    f"Category: {entry['category']} | Question: {entry['question']} | Options: {', '.join(entry['options'])}"
    for entry in corpus
]

# Generate embeddings
embeddings = model.encode(texts, convert_to_numpy=True)
print(embeddings)

# Get embedding dimensions (e.g., 384 for all-MiniLM-L6-v2)
dim = embeddings.shape[1]
# print(dim)