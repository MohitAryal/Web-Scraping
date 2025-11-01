from sentence_transformers import SentenceTransformer, util
import torch

# Load pre-trained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def find_top_results(intent: str, links: list[str]) -> list[str]:

    print("[INFO] Encoding the user's intent and webpage content.")
    # Encode user intent and webpage content (URLs or metadata)
    intent_emb = model.encode(intent, convert_to_tensor=True)
    page_embs = model.encode(links, convert_to_tensor=True)

    # Compute cosine similarities
    similarities = util.cos_sim(intent_emb, page_embs)[0]

    # Sort by similarity and get top 5
    top_indices = torch.topk(similarities, k=min(5, len(links))).indices.tolist()
    top_links = [links[i] for i in top_indices]

    # Return the top links
    return top_links