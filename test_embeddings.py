from sentence_transformers import SentenceTransformer
import numpy as np

def test_model():
    print("Loading the model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Test sentences
    sentences = [
        "RecoGenie provides AI solutions for businesses",
        "What are your pricing plans?",
        "Tell me about your customer support"
    ]
    
    print("\nGenerating embeddings...")
    embeddings = model.encode(sentences)
    
    print("\nEmbeddings shape:", embeddings.shape)
    print("Number of sentences:", len(sentences))
    print("Embedding dimension:", embeddings.shape[1])
    
    # Test similarity
    print("\nTesting similarity between sentences:")
    for i in range(len(sentences)):
        for j in range(i+1, len(sentences)):
            similarity = np.dot(embeddings[i], embeddings[j]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j]))
            print(f"Similarity between '{sentences[i]}' and '{sentences[j]}': {similarity:.4f}")

if __name__ == "__main__":
    test_model() 