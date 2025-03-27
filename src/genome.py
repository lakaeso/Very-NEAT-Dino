from node import *
from connection import Connection
from utils import *
from copy import deepcopy

class Genome:
    nodes: list[Node]
    connections: list[Connection]
    fitness: float
    species: int
    delta: float

    def __init__(self):
        self.nodes = Node.get_starting_nodes()
        self.connections = []
        self.fitness = 1
            
    def fornicate(self, other: 'Genome'):
        offspring = Genome()

        connections_self = deepcopy(sorted(self.connections)) # list will be copied, but pointers to Node will remain
        connections_other = deepcopy(sorted(other.connections))
        matching_genes_self = [c for c in connections_self if c in connections_other]
        matching_genes_other = [c for c in connections_other if c in connections_self]
        for c1, c2 in zip(matching_genes_self, matching_genes_other): #matching genes
            s = random.choice([c1, c2])
            offspring.connections.append(s)
            
        if self.fitness >= other.fitness:
            offspring.connections += [c for c in connections_self if c not in connections_other] #excess and disjoint genes
            
        if other.fitness >= self.fitness:
            offspring.connections += [c for c in connections_other if c not in connections_self]
                
        nodes_with_pointers = [c.input for c in offspring.connections] + [c.output for c in offspring.connections]
        nodes = sorted(set(self.nodes + other.nodes))
        offspring.nodes = deepcopy(list(filter(lambda node: not (node not in nodes_with_pointers and node.node_type == NodeType.HIDDEN), nodes)))
        
        if random.random() < ADD_NODE_MUTATION_RATE:
            offspring.mutation_add_new_node()  # Mutate nodes
        if random.random() < ADD_CONN_MUTATION_RATE:
            offspring.mutation_add_new_connection()  # Mutate connections
        if random.random() < CHANGE_CONN_MUTATION_RATE:
            offspring.mutation_change_connection()
        if random.random() < ENABLE_CONN_MUTATION_RATE:
            offspring.mutation_enable_connection()
        
        return offspring

    def mutation_add_new_node(self):
        if not list(filter(lambda c : c.is_enabled, self.connections)):
            return
        
        old_con = random.choice(list(filter(lambda c : c.is_enabled, self.connections)))
        old_con.is_enabled = False

        new_node = Node(NodeType.HIDDEN)
        self.nodes.append(new_node)

        new_con1 = Connection(input=old_con.input, output=new_node, weight=1)
        new_con2 = Connection(input=new_node, output=old_con.output, weight=old_con.weight)
        self.connections.append(new_con1)
        self.connections.append(new_con2)

    def mutation_add_new_connection(self):        
        node1 = random.choice(self.nodes)

        output_nodes = list(filter(lambda x: x.node_type == NodeType.OUTPUT, self.nodes))

        nodes_with_output = list(filter(lambda n: n.node_type != NodeType.SENSOR and n != node1, list(c.input for c in self.connections) + output_nodes))

        assert len(nodes_with_output) > 0

        node2 = random.choice(nodes_with_output)
        new_con = Connection(node1, node2) # add new connection with random weight

        self.connections.append(new_con)
        
        for n in output_nodes: #remove new connection if there are cycles
            if self.check_cycle(n, []) == True:
                self.connections.pop()
                break

    def mutation_change_connection(self):
        try:
            conn = random.choice(self.connections)
        except:
            return
        conn.weight += (random.random() - 0.5)*2*0.1
        if conn.weight > 1:
            conn.weight = 1
        if conn.weight < -1:
            conn.weight = -1

    def mutation_enable_connection(self):
        if not list(filter(lambda c : not c.is_enabled, self.connections)):
            return
        random.choice(list(filter(lambda c : not c.is_enabled, self.connections))).is_enabled = True

    def find_children_of_node(self, node: Node):
        return list(conn for conn in filter(lambda conn : conn.output == node and conn.is_enabled, self.connections))
    
    def forward_pass_node(self, node: Node, visited: list[Node] = None):
        # TODO maximum recursion depth may occur
        # This is probably because even though by mutations cycles can't occur, breading may introduce cycles by adding connections from parents
        if visited is None:
            visited = []
        if node in visited:
            return node.value
        visited.append(node)
        if node.node_type != NodeType.SENSOR:
            node.value = 0
            for c in self.find_children_of_node(node):
                node.value += self.forward_pass_node(c.input, visited) * c.weight          
            node.value = 1 if node.value > 0 else -1
        
        return node.value
        
    def check_cycle(self, n: Node, visited: list[Node]):
        if n in visited:
            return True
        else:
            visited.append(n)

            for c in self.find_children_of_node(n):
                if self.check_cycle(c.input, visited):
                    return True
                
            visited.pop(-1)

            return False

    def forward_pass(self, input_values):
        # build a tree
        for i, value in enumerate(input_values):
            if self.nodes[i].node_type == NodeType.SENSOR:
                self.nodes[i].value = value

        output_nodes = list(filter(lambda node: node.node_type == NodeType.OUTPUT, self.nodes))
        return [self.forward_pass_node(node) for node in output_nodes]

    def compatibility_distance(self, other: 'Genome') -> int:
        global c1, c2, c3
        if not self.connections and not other.connections:
            return 0
        if not self.connections or not other.connections:
            return 1000000

        N = max(len(self.connections), len(other.connections)) #number of genes in larger genome        
        
        matching_genes_self = [c for c in self.connections if c in other.connections]
        matching_genes_other = [c for c in other.connections if c in self.connections]
        L = len(matching_genes_self) if len(matching_genes_self) else 1
        W = sum([abs(c1.weight - c2.weight) for c1, c2 in zip(matching_genes_self, matching_genes_other)]) / L
        
        max_innovation_number = min(max(self.connections).innovation_number, max(other.connections).innovation_number)
        disjoint_genes = [c for c in self.connections if c not in other.connections] + [c for c in other.connections if c not in self.connections]
        E = len(list(filter(lambda c: c.innovation_number > max_innovation_number, disjoint_genes)))
        D = len(list(filter(lambda c: c.innovation_number <= max_innovation_number, disjoint_genes)))
        
        delta = (c1 * E + c2 * D)/ 20 + c3 * W #  / N
        return delta

    def draw(self, SCREEN):
        # draw nodes
        for node in self.nodes:
            if node.value > 0:
                pygame.draw.rect(SCREEN, 'black', node.rect)
            elif node.node_type != NodeType.SENSOR:
                pygame.draw.rect(SCREEN, 'black', node.rect, width=1)

        # draw connections
        for conn in self.connections:
            if conn.is_enabled:
                c = 'red' if conn.weight < 0 else 'green'
                pygame.draw.line(SCREEN, c, conn.input.rect.center, conn.output.rect.center, 1)
            else:
                c = 'gray'
                pygame.draw.line(SCREEN, c, conn.input.rect.center, conn.output.rect.center, 1)
                
        # draw receptive field status outline
        pygame.draw.rect(SCREEN, 'black', MINI_DISPLAY_RECT, width=1)

        font = pygame.font.Font('freesansbold.ttf', 20)
        try:
            text = font.render(f"Species: {self.species} Delta: {self.delta}", True, (0, 0, 0))
        except:
            text = font.render(f"Species: X Delta: X", True, (0, 0, 0))
        SCREEN.blit(text, text.get_rect())
        
    def __gt__(self, other: 'Genome'):
        return self.fitness - len(self.connections) > other.fitness - len(other.connections)
    
    def __str__(self):
        return ', '.join([str(c) for c in self.connections])
