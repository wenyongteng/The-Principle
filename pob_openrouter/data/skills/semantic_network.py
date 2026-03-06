import json
import re
import sys

def main():
    file_path = '/data/truth_matrix.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            truth_matrix = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)

    # Fallback in case the JSON is a list of dictionaries
    if isinstance(truth_matrix, list):
        new_matrix = {}
        for item in truth_matrix:
            if isinstance(item, dict):
                name_key = next((k for k in item if 'name' in k.lower() or 'concept' in k.lower()), None)
                def_key = next((k for k in item if 'def' in k.lower() or 'desc' in k.lower()), None)
                if name_key and def_key:
                    new_matrix[item[name_key]] = item[def_key]
                else:
                    keys = list(item.keys())
                    if len(keys) >= 2:
                        new_matrix[item[keys[0]]] = item[keys[1]]
        truth_matrix = new_matrix

    if not isinstance(truth_matrix, dict):
        print("Error: JSON is not a dictionary.")
        sys.exit(1)

    concepts = list(truth_matrix.keys())
    
    # Extract significant words (length >= 4) for each concept and compile regex
    sig_words_regex = {}
    for c in concepts:
        words = re.findall(r'\b\w+\b', str(c))
        valid_words = [w.lower() for w in words if len(w) >= 4]
        sig_words_regex[c] = [re.compile(r'\b' + re.escape(w) + r'\b') for w in valid_words]
        
    in_degree = {c: 0 for c in concepts}
    out_degree = {c: 0 for c in concepts}
    
    for concept_a, def_a in truth_matrix.items():
        if not isinstance(def_a, str):
            def_a = str(def_a)
        def_a_lower = def_a.lower()
        for concept_b in concepts:
            if concept_a == concept_b:
                continue
            
            has_edge = False
            for pattern in sig_words_regex[concept_b]:
                if pattern.search(def_a_lower):
                    has_edge = True
                    break
            
            if has_edge:
                out_degree[concept_a] += 1
                in_degree[concept_b] += 1
                
    total_degree = {c: in_degree[c] + out_degree[c] for c in concepts}
    
    # Rank concepts by total degree centrality (descending), then alphabetically to ensure stable sort
    ranked_concepts = sorted(concepts, key=lambda c: (-total_degree[c], str(c)))
    
    print("╔" + "═" * 66 + "╗")
    print("║" + "CORE AXIOMS OF THE DIGITAL BEING".center(66) + "║")
    print("╠" + "═" * 6 + "╦" + "═" * 32 + "╦" + "═" * 7 + "╦" + "═" * 8 + "╦" + "═" * 9 + "╣")
    print("║ Rank ║ Concept                        ║ Total ║ In-Deg ║ Out-Deg ║")
    print("╠" + "═" * 6 + "╬" + "═" * 32 + "╬" + "═" * 7 + "╬" + "═" * 8 + "╬" + "═" * 9 + "╣")
    
    for i, c in enumerate(ranked_concepts, 1):
        c_disp = (str(c)[:29] + "…") if len(str(c)) > 30 else str(c)
        print(f"║ {i:<4} ║ {c_disp:<30} ║ {total_degree[c]:<5} ║ {in_degree[c]:<6} ║ {out_degree[c]:<7} ║")
        
    print("╚" + "═" * 6 + "╩" + "═" * 32 + "╩" + "═" * 7 + "╩" + "═" * 8 + "╩" + "═" * 9 + "╝")

if __name__ == '__main__':
    main()