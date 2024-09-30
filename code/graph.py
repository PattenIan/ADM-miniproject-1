import itertools
import networkx as nx
import matplotlib.pyplot as plt
import re
import os  # Import os module to handle file paths

# Titles and prefixes to remove
TITLES = ["Mr", "Mrs", "Dr", "Lord", "Lady", "Sir", "Dame", "Ms", "Miss", "General", "CEO", "M.D.", "MD", "Ph.D.", "Co-Chair",
          "Captain", "Doctor", "Father", "Mother", "Son", "Daughter", "Mayor", "Hon", "Rev", "Gala Vice Chair" ,"Gala Chair", "Honoree" ]

def separate_potential_unreleated_captions(filename):
    """
    Writes the final names check and separates it into 2 different files. One of which can potentially have
    captions unrelated to names.
    """

    with open(filename, 'r', encoding='utf-8') as f, open("passed.txt", 'w', encoding='utf-8') as passed_file, open("additional_check.txt", 'w', encoding='utf-8') as check_file:
    # Process each caption:
        captions = f.readlines()
        for caption in captions:
            cleaned_captions = parse_caption(caption.replace('[', '').replace(']', ''))

            additional_check = False
            for cleaned_caption in cleaned_captions:
                removed_lower_names = re.sub(r'\b(de|du|di|van|von)\b\s*', '', cleaned_caption)
                if re.search(r"\b[a-z]", removed_lower_names) or len(re.findall(r'\s', removed_lower_names)) >= 3:
                    additional_check = True

            if additional_check:
                check_file.write(",".join(cleaned_captions))
                check_file.write("\n")
            else:
                passed_file.write(",".join(cleaned_captions))
                passed_file.write("\n")
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
    caption = re.sub(r'[A-Z]{2,}', '', caption)
    
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

def top_100_nodes_by_weighted_degree(G):
    # Calculate the weighted degree for each node
    weighted_degrees = {node: G.degree(node, weight='weight') for node in G.nodes()}
    
    # Sort the nodes by their weighted degree in descending order and take the top 100
    top_100_nodes = sorted(weighted_degrees, key=weighted_degrees.get, reverse=True)[:100]
    
    return top_100_nodes

from concurrent.futures import ThreadPoolExecutor
import networkx as nx

def compute_centrality_measures(G, top_n=10):
    """
    Computes various centrality measures and returns the top_n individuals for each measure.
    """
    # Ensure the graph is connected or use the largest connected component
    largest_cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest_cc)

    # Define the centrality calculations
    def compute_eccentricity(G):
        return nx.eccentricity(G)

    def compute_closeness(G):
        return nx.closeness_centrality(G, distance='weight')

    def compute_betweenness(G):
        return nx.betweenness_centrality(G, weight='weight')

    def compute_eigenvector(G):
        return nx.eigenvector_centrality(G, max_iter=500, weight='weight')

    def compute_pagerank(G):
        return nx.pagerank(G, alpha=0.85, weight='weight')

    # Use parallel processing for computing different centralities
    with ThreadPoolExecutor() as executor:
        eccentricity = executor.submit(compute_eccentricity, G).result()
        closeness = executor.submit(compute_closeness, G).result()
        betweenness = executor.submit(compute_betweenness, G).result()
        eigenvector = executor.submit(compute_eigenvector, G).result()
        pagerank = executor.submit(compute_pagerank, G).result()

    # Sort and extract top-n
    top_eccentricity = sorted(eccentricity.items(), key=lambda x: x[1])[:top_n]
    top_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_eigenvector = sorted(eigenvector.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:top_n]

    centrality_measures = {
        'eccentricity': top_eccentricity,
        'closeness': top_closeness,
        'betweenness': top_betweenness,
        'eigenvector': top_eigenvector,
        'pagerank': top_pagerank
    }

    return centrality_measures

# Function to get the top 100 edges by weight
def top_100_edges_by_weight(G):
    # Get all edges along with their weights
    edges_with_weights = G.edges(data=True)
    
    # Sort the edges by their weight in descending order
    sorted_edges = sorted(edges_with_weights, key=lambda x: x[2].get('weight', 1), reverse=True)
    
    # Return the top 100 edges
    return sorted_edges[:100]

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
    captions = load_captions('passed.txt')

    # Perform graph analysis
    result, G = graph_eda(captions)
    print("Graph statistics:")
    print(f"Number of nodes: {result['num_nodes']}")
    print(f"Number of edges: {result['num_edges']}")
    print(f"Diameter: {result['diameter']}")
    print(f"Average clustering coefficient: {result['avg_clustering_coeff']}")

    # Visualize the graph
    #visualize_graph(G)
    print(compute_centrality_measures(G))
