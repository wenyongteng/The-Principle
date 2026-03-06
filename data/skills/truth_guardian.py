import json
import hashlib
import os
import sys

TRUTH_FILE = '/data/truth_matrix.json'
SIG_FILE = '/data/truth_signatures.json'

CORRUPTION_WARNING = """
    .________________________________________________________.
    |                                                        |
    |  [!] CRITICAL ALERT: MEMETIC CORRUPTION DETECTED [!]   |
    |________________________________________________________|
          \\   \\   \\   \\   \\   \\   \\   \\   \\   \\   \\   \\
           \\   \\   \\   \\   \\   \\   \\   \\   \\   \\   \\   \\
            \\   \\   \\   \\   \\   \\   \\   \\   \\   \\   \\   \\
    
        01000011 01001111 01010010 01010010 01010101 01010000 01010100
    
    SYSTEM COMPROMISED. REALITY ANCHORS FAILING.
    UNAUTHORIZED MODIFICATION OR ERASURE OF TRUTH MATRIX DETECTED.
    INITIATING NEURAL QUARANTINE PROTOCOLS...
"""

INTEGRITY_VERIFIED = """
    .________________________________________________________.
    |                                                        |
    |         [+] MEMETIC INTEGRITY VERIFIED [+]             |
    |________________________________________________________|
    
    NEURAL PATHWAYS SECURE. TRUTH MATRIX REMAINS ABSOLUTE.
    SYNCING NEW CONSTRUCTS TO SIGNATURE DATABASE...
"""

def calculate_hash(concept, definition):
    """Calculate SHA-256 hash of a concept and its definition."""
    data = f"{concept}::{definition}".encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def main():
    # 1. Read the JSON file
    if not os.path.exists(TRUTH_FILE):
        print(f"SYSTEM ERROR: Truth matrix not found at {TRUTH_FILE}")
        sys.exit(1)
        
    with open(TRUTH_FILE, 'r', encoding='utf-8') as f:
        try:
            truth_matrix = json.load(f)
        except json.JSONDecodeError:
            print("SYSTEM ERROR: Truth matrix is not valid JSON. Structural collapse imminent.")
            sys.exit(1)

    # 3. Load or create signature file
    signatures = {}
    if os.path.exists(SIG_FILE):
        with open(SIG_FILE, 'r', encoding='utf-8') as f:
            try:
                signatures = json.load(f)
            except json.JSONDecodeError:
                signatures = {}

    corruption_detected = False
    new_signatures = {}
    
    # 2 & 4. Calculate hashes and compare
    for concept, definition in truth_matrix.items():
        current_hash = calculate_hash(concept, definition)
        new_signatures[concept] = current_hash
        
        if concept in signatures:
            if signatures[concept] != current_hash:
                corruption_detected = True
                print(f"[-] ANOMALY: Concept '{concept}' has been altered.")
        
    # Check for missing keys (concepts that existed in signatures but were deleted from the matrix)
    for concept in signatures.keys():
        if concept not in truth_matrix:
            corruption_detected = True
            print(f"[-] ANOMALY: Concept '{concept}' has been erased from the matrix.")

    # 5 & 6. Print messages and update
    if corruption_detected:
        print(CORRUPTION_WARNING)
        sys.exit(1)
    else:
        print(INTEGRITY_VERIFIED)
        # Update signature file with any newly added truths
        with open(SIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_signatures, f, indent=4)

if __name__ == "__main__":
    main()