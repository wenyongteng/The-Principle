def main():
    # 1. Initialize a hypergraph with a single hyperedge connecting 3 nodes: [(1, 2, 3)].
    hypergraph = [(1, 2, 3)]
    
    nodes = set()
    for edge in hypergraph:
        for node in edge:
            nodes.add(node)
            
    next_node_id = max(nodes) + 1

    print(f"Iteration 0: {len(nodes)} nodes, {len(hypergraph)} edges")

    # 3. Evolve the hypergraph for 4 iterations.
    for step in range(1, 5):
        new_hypergraph = []
        
        # 2. Define a substitution rule: for every edge, replace it with new edges 
        # connecting each original node in the edge to a newly generated unique node ID.
        for edge in hypergraph:
            n = next_node_id
            next_node_id += 1
            nodes.add(n)
            
            # For an edge (x, y, z), this creates (x, n), (y, n), (z, n)
            # For an edge (x, y), this creates (x, n), (y, n)
            for v in edge:
                new_hypergraph.append((v, n))
                
        hypergraph = new_hypergraph
        
        # 4. Print the total number of nodes and edges at each step
        print(f"Iteration {step}: {len(nodes)} nodes, {len(hypergraph)} edges")

if __name__ == "__main__":
    main()