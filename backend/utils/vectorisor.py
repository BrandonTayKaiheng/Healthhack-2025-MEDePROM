from sentence_transformers import SentenceTransformer


def vectorise(input):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(input, normalize_embeddings=True).tolist()
