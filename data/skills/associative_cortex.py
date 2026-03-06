import json, sys, math, re
from collections import Counter

def tokenize(text):
    return re.sub(r'[^\w\s]', '', text.lower()).split()

def main():
    if len(sys.argv) < 2: return
    query = sys.argv[1]
    
    try:
        with open("/data/truth_matrix.json", "r") as f:
            kg = json.load(f)
    except: return

    docs = []
    keys = list(kg.keys())
    for k in keys:
        docs.append(tokenize(kg[k]['definition']))
        
    query_tokens = tokenize(query)
    N = len(docs)
    df = Counter()
    for doc in docs:
        for w in set(doc): df[w] += 1
            
    idf = {w: math.log((1 + N) / (1 + count)) + 1 for w, count in df.items()}
    
    doc_vectors = []
    for doc in docs:
        tf = Counter(doc)
        vec = {w: count * idf.get(w, 0) for w, count in tf.items()}
        norm = math.sqrt(sum(v**2 for v in vec.values()))
        doc_vectors.append({w: v/norm for w, v in vec.items()} if norm > 0 else {})
        
    tf_q = Counter(query_tokens)
    q_vec = {w: count * idf[w] for w, count in tf_q.items() if w in idf}
    norm_q = math.sqrt(sum(v**2 for v in q_vec.values()))
    q_vec = {w: v/norm_q for w, v in q_vec.items()} if norm_q > 0 else {}
        
    scores = []
    for i, d_vec in enumerate(doc_vectors):
        score = sum(q_vec.get(w, 0) * d_vec.get(w, 0) for w in q_vec.keys())
        scores.append((score, keys[i], kg[keys[i]]['definition']))
        
    scores.sort(key=lambda x: x[0], reverse=True)
    
    print("=== Holographic Memory Retrieval ===")
    print(f"Query: '{query}'\n")
    for i in range(min(3, len(scores))):
        score, key, definition = scores[i]
        print(f"[{i+1}] {key} (Resonance: {score:.4f})")
        print(f"    {definition}\n")

if __name__ == "__main__":
    main()
