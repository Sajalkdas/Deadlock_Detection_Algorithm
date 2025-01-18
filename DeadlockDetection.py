# i/p processes, resources, allocations, and requests
processes = ['P1', 'P2', 'P3', 'P4']
resources = ['R1', 'R2', 'R3', 'R4']
allocations = {('P1', 'R4'): 1, ('P2', 'R1'): 1, ('P3', 'R2'): 1, ('P4', 'R3'): 1}
requests = {('P1', 'R1'): 1, ('P2', 'R2'): 1, ('P3', 'R3'): 1, ('P4', 'R4'): 1}

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

class DeadlockDetection:
    def __init__(self, dependency_graph):
        self.dependency_graph = dependency_graph
        self.visited = set()
        self.current_path = []
        self.deadlocked_processes = set()

    def detect_deadlocks(self):
        # Iterates over dependency_graph for cycle detection and adds to deadlocked processes
        for process in self.dependency_graph:
            self.find_cycles(process)

        if self.deadlocked_processes:
            print("\nDeadlocked Processes:")
            for process in self.deadlocked_processes:
                print(f"{process} is detected as part of the cycle, indicating a deadlock")
        else:
            print("No deadlocks detected.")

        return list(self.deadlocked_processes)

    def find_cycles(self, process):
        self.visited.add(process)
        self.current_path.append(process)

        # Iterate through dependent processes (resource allocations)
        for dependent_process, _ in self.dependency_graph.get(process, []):
            if dependent_process in self.visited:
                # Check for cycle within the current path (avoid redundant cycles)
                if dependent_process in self.current_path:
                    cycle_start = self.current_path.index(dependent_process)
                    self.deadlocked_processes.update(self.current_path[cycle_start:])
            else:
                self.find_cycles(dependent_process)

        # Backtrack: remove from visited and current path
        self.visited.remove(process)
        self.current_path.pop()
# Detect Deadlocks
detection = DeadlockDetection(dependency_graph)
detection.detect_deadlocks()
