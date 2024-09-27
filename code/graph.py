import itertools
import networkx as nx
import matplotlib.pyplot as plt
import re
import os  # Import os module to handle file paths

# Titles and prefixes to remove
TITLES = ["Mr", "Mrs", "Dr", "Lord", "Lady", "Sir", "Dame", "Ms", "Miss", "General", "CEO", "M.D.", "Ph.D.", "Co-Chair",
          "Captain", "Doctor", "Father", "Mother", "Son", "Daughter", "Mayor", "Hon", "Rev"]

def separate_potential_unreleated_captions(filename):
    """
    Writes the final names check and separates it into 2 different files. One of which can potentially have
    captions unrelated to names.
    """

    with open(filename, 'r', encoding='utf-8') as f, open("passed", 'w', encoding='utf-8') as passed_file, open("additional_check", 'w', encoding='utf-8') as check_file:
    # Process each caption:
        captions = f.readlines()
        for caption in captions:
            cleaned_captions = parse_caption(caption.replace('[', '').replace(']', ''))

            for cleaned_caption in cleaned_captions:
                removed_lower_names = re.sub(r'\b(de|du|di|van|von)\b\s*', '', cleaned_caption)
                if re.search(r"\b[a-z]", removed_lower_names):
                    check_file.write(cleaned_caption + '\n')
                else:
                    passed_file.write(cleaned_caption + '\n')

def load_captions(filename):
    """
    Load the captions from a file and return as a list of strings.
    """
    # Get the absolute path of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the captions file
    filepath = os.path.join(current_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.readlines()

def parse_caption(caption):
    """
    Parses a caption string into a list of names.
    - Handles names like "John and Jane Doe" by splitting them.
    - Removes titles (Mr, Mrs, Dr, etc.).
    """
    # Replace ' and ' with ', ' to make it easier to split
    caption = caption.replace(' and ', ', ')
    caption = caption.replace('; ', ', ')
    # Remove anything unrelated in ()
    caption = re.sub(r'\s*\([^)]*\)', '', caption)
    
    # Split the caption into names
    names = [name.strip() for name in caption.split(',') if name.strip()]

    # Clean each name and filter out titles
    cleaned_names = []
    for name in names:
        # Remove titles
        words = name.split()
        words = [word for word in words if word not in TITLES]
        cleaned_name = " ".join(words)
        cleaned_names.append(cleaned_name)
    
    return cleaned_names

def graph_eda(captions):
    """
    Creates an undirected weighted graph from the list of captions.
    Returns graph statistics and the graph object.
    """
    G = nx.Graph()

    # Build the graph
    for caption in captions:
        names = parse_caption(caption)
        if len(names) > 1:
            for pair in itertools.combinations(names, 2):
                # Increment edge weight if edge exists, else create it
                if G.has_edge(pair[0], pair[1]):
                    G[pair[0]][pair[1]]['weight'] += 1
                else:
                    G.add_edge(pair[0], pair[1], weight=1)

    # Calculate graph statistics
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    # Diameter calculation
    if nx.is_connected(G):
        diameter = nx.diameter(G)
    else:
        # Use the largest connected component
        largest_cc = max(nx.connected_components(G), key=len)
        diameter = nx.diameter(G.subgraph(largest_cc))

    # Average clustering coefficient
    avg_clustering_coeff = nx.average_clustering(G)

    graph_stats = {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "diameter": diameter,
        "avg_clustering_coeff": avg_clustering_coeff
    }

    return graph_stats, G

def visualize_graph(G):
    """
    Visualizes the graph using a spring layout.
    For large graphs, it visualizes a subgraph of up to 100 nodes.
    """
    # Visualize a subgraph if the graph is too large
    subgraph = G
    if G.number_of_nodes() > 100:
        # Largest connected component
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc)
        # Limit to 100 nodes
        if subgraph.number_of_nodes() > 100:
            subgraph = subgraph.subgraph(list(subgraph.nodes())[:100])

    pos = nx.spring_layout(subgraph)

    # Draw nodes and edges
    nx.draw_networkx_nodes(subgraph, pos, node_size=300, node_color='lightblue')
    nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(subgraph, pos, font_size=8)

    # Add edge weights as labels
    edge_labels = {(u, v): d['weight'] for u, v, d in subgraph.edges(data=True)}
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=6)

    plt.title("Graph Visualization")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Load captions from the text file
    captions = load_captions('captions.txt')

    # Perform graph analysis
    result, G = graph_eda(captions)
    print("Graph statistics:")
    print(f"Number of nodes: {result['num_nodes']}")
    print(f"Number of edges: {result['num_edges']}")
    print(f"Diameter: {result['diameter']}")
    print(f"Average clustering coefficient: {result['avg_clustering_coeff']}")

    # Visualize the graph
    visualize_graph(G)
