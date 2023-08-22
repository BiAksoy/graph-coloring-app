import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt


class GraphColoringApp:
    def __init__(self):
        self.graph = nx.Graph()
        self.node_colors = {}
        self.available_colors = []

        self.root = tk.Tk()
        self.root.title("Graph Coloring App")
        self.root.geometry("600x400")

        self.node_entry = tk.Text(self.root, height=8, width=40)
        self.node_entry_label = tk.Label(self.root, text="Enter nodes (one node per line):")
        self.node_entry_label.pack()
        self.node_entry.pack()

        self.save_nodes_button = tk.Button(self.root, text="Save Nodes", command=self.save_nodes)
        self.save_nodes_button.pack()

        self.add_edges_button = tk.Button(self.root, text="Add Edges", command=self.open_edge_entry_window)
        self.add_edges_button.pack()

    def save_nodes(self):
        nodes_text = self.node_entry.get(1.0, tk.END)
        with open("nodes.txt", "w") as file:
            file.write(nodes_text)

    def open_edge_entry_window(self):
        edge_entry_window = tk.Toplevel(self.root)
        edge_entry_window.title("Edge Entry")
        edge_entry_window.geometry("600x400")

        self.edge_entry = tk.Text(edge_entry_window, height=8, width=40)
        self.edge_entry_label = tk.Label(edge_entry_window, text="Enter edges (one edge per line):")
        self.edge_entry_label.pack()
        self.edge_entry.pack()

        save_edges_button = tk.Button(edge_entry_window, text="Save Edges", command=self.save_edges)
        save_edges_button.pack()

        select_colors_button = tk.Button(edge_entry_window, text="Select Colors", command=self.start_coloring_process)
        select_colors_button.pack()

    def save_edges(self):
        edges_text = self.edge_entry.get(1.0, tk.END)
        with open("edges.txt", "w") as file:
            file.write(edges_text)

    def start_coloring_process(self):
        colors_entry_window = tk.Toplevel(self.root)
        colors_entry_window.title("Select Colors")
        colors_entry_window.geometry("600x400")

        self.colors_entry = tk.Text(colors_entry_window, height=8, width=40)
        self.colors_entry_label = tk.Label(colors_entry_window, text="Enter available colors (comma-separated):")
        self.colors_entry_label.pack()
        self.colors_entry.pack()

        colors_instruction = tk.Label(colors_entry_window,
                                      text="Please enter node colors separated by commas (e.g., red,green,blue).")
        colors_instruction.pack()

        color_list_label = tk.Label(colors_entry_window,
                                    text="Color list: blue, brown, cyan, gray, green, orange, pink, purple, red, yellow.")
        color_list_label.pack()

        save_colors_button = tk.Button(colors_entry_window, text="Save Colors", command=self.apply_colors)
        save_colors_button.pack()

    def apply_colors(self):
        colors_text = self.colors_entry.get(1.0, tk.END)
        self.available_colors = [color.strip() for color in colors_text.split(",")]

        self.graph.clear()
        self.node_colors.clear()

        edges = nx.read_edgelist("edges.txt")
        nodes = nx.read_adjlist("nodes.txt")

        self.graph.add_edges_from(edges.edges())
        self.graph.add_nodes_from(nodes)

        new_graph = nx.Graph()
        filled_colors = []

        for node in self.graph.nodes:
            self.node_colors[node] = self.choose_color(node)
            given_color = str(self.node_colors[node])
            new_graph.add_node(node, color=given_color, style='filled')
            filled_colors.append(given_color)
            nx.draw_networkx(new_graph, node_color=filled_colors, with_labels=True)
            plt.show(block=False)
            plt.pause(0.2)
            plt.close()

        new_graph.add_edges_from(edges.edges())
        nx.draw_networkx(self.graph, node_color=filled_colors, with_labels=True)
        plt.show()

    def choose_color(self, node):
        for color in self.available_colors:
            if self.is_valid_color(node, color):
                return color

    def is_valid_color(self, node, color):
        for neighbor in list(self.graph.neighbors(node)):
            neighbor_color = self.node_colors.get(neighbor)
            if neighbor_color == color:
                return False
        return True

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GraphColoringApp()
    app.run()
