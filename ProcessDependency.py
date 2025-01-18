# # i/p  processes, resources, allocations, and requests
processes = ['P1', 'P2', 'P3', 'P4']
resources = ['R1', 'R2']
allocations = {('P1', 'R1'): 1, ('P2', 'R2'): 1}
requests = {('P3', 'R1'): 1, ('P3', 'R2'): 1, ('P4', 'R2'): 1}


class GraphReduction:
    def __init__(self, processes, resources, allocations, requests):
        self.processes = processes
        self.resources = resources
        self.allocations = allocations
        self.requests = requests

    def reduce_graph(self):
        dependency_graph = {p: set() for p in self.processes}
        # Iterates over processes & resources, looks for allocation and adds to dependency graph
        for p in self.processes:
            for r in self.resources:
                if self.requests.get((p, r), 0) > 0:
                    for alloc_p in self.processes:
                        if self.allocations.get((alloc_p, r), 0) > 0:
                            dependency_graph[p].add((alloc_p, r))

        return dependency_graph


def print_dependency_graph(dependency_graph):
    print("\nProcesses Dependency Graphs:")
    for process in dependency_graph:
        if dependency_graph[process]:
            for dep, res in dependency_graph[process]:
                print(f"{process} depends on {dep} because {process} has requested resource {res} which is allocated to {dep}.")
        else:
            print(f"{process} has no dependencies.")


# Perform Graph Reduction to get the dependency graph
reduction = GraphReduction(processes, resources, allocations, requests)
dependency_graph = reduction.reduce_graph()

# Print Dependency Graph
print_dependency_graph(dependency_graph)


