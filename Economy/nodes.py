
import numpy as np
import json

class Node:
    def __init__(self, name, amount = 0, production = 1, price = 1):
        self.name = name
        self.amount = amount
        self.production = production
        self.price = price

    def print(self):
        print('{}:: amount: {}, production: {}, price: {}'.format(self.name, self.amount, self.production, self.price))

    def to_json(self, network):
        j = network.get_index(self)
        return {'name': self.name, 'amount': self.amount, 'production': self.production, 'price': self.price,
                'connections': [{'target': int(i), 'weight': network.connections[j, i]} for i in np.where(network.connections[j, :] > 0)[0]]}

    @staticmethod
    def from_json(data):
        return Node(data['name'], data['amount'], data['production'], data['price'])

class Network:
    def __init__(self, number_nodes):
        self.connections = np.zeros(shape=(number_nodes, number_nodes))
        self.nodes = np.ndarray(shape=(number_nodes,), dtype=object)

        for i in range(number_nodes):
            self.nodes[i] = Node('node_{}'.format(i))

        self.time = 0
        self.waves = list()

    def get_number_nodes(self):
        return len(self.nodes)

    @staticmethod
    def from_json(data):
        n = len(data['nodes'])
        network = Network(n)
        connections = np.zeros(shape=(n, n))
        
        for i in range(n):
            network.nodes[i] = Node.from_json(data['nodes'][i])

            for con in data['nodes'][i]['connections']:
                connections[i, con['target']] = con['weight']

        network.connections = connections
        return network

    def print(self):
        n = len(self.nodes)
        print('time: {}'.format(self.time))
        indices = np.arange(n)
        
        for i in range(n):
            self.nodes[i].print()

            #cns = np.where(self.connections[i, :] > 0)
            #print('\tconnected to nodes: {}'.format(', '.join([str(x) for x in cns])))

        print(self.connections)

    def get_index(self, node):
        i, = np.where(self.nodes == node)[0]
        return int(i)

    def perform_step(self):
        self.time += 1

        # update production
        to_remove = list()

        for wave in self.waves:
            wave.perform_step(self)
            if (wave.finished):
                to_remove.append(wave)

        for wave in to_remove:
            self.waves.remove(wave)

        # update amounts
        self.update_amounts()

    def applyWave(self, wave):
        self.waves.append(wave)
        wave.start.production *= wave.productionFactor

    def update_amounts(self):
        n = len(self.nodes)

        for i in range(n):
            indices = np.where(self.connections[:, i] > 0)[0]

            valid = True
            for j in indices:
                valid = valid and (self.nodes[j].amount - self.connections[j, i] >= 0)

            if (valid):
                for j in indices:
                    self.nodes[j].amount -= self.connections[j, i]

                self.nodes[i].amount += self.nodes[i].production

class NetworkEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Network):
            n = obj.get_number_nodes()
            return {'nodes': [node.to_json(obj) for node in obj.nodes]}
        else:
            return json.JSONEncoder.default(self, obj)

class Wave:
    def __init__(self, node, factor):
        self.start = node
        self.productionFactor = factor

        self.visited = list()
        self.visiting = list()
        self.visiting.append(node)
        self.finished = False

    def perform_step(self, network):
        if (len(self.visiting) > 0):
            newVisits = list()

            for node in self.visiting:
                i = network.get_index(node)

                for j in range(len(network.connections[:, i])):
                    if (network.connections[j, i] > 0 and network.nodes[j] not in self.visited and network.nodes[j] not in newVisits):
                        newVisits.append(network.nodes[j])
                        network.nodes[j].production *= self.productionFactor

                self.visited.append(node)
            
            self.visiting = newVisits

# n = Network(6)

# n.nodes[0].name = 'Eisenerz'
# n.nodes[0].production = 2

# n.nodes[1].name = '...'
# n.nodes[2].production = 2

# n.connections[0, 3] = 5
# n.connections[3, 5] = 5
# n.connections[1, 4] = 5
# n.connections[1, 3] = 5
# n.connections[2, 4] = 5
# n.connections[4, 5] = 5

# for i in range(6):
#    n.nodes[i].production = 7

# with open('nodes.json', 'w') as f:
#     f.write(json.dumps(n, indent=4, cls=NetworkEncoder))

# n.print()

n = None

with open('nodes.json') as json_data:
    d = json.load(json_data)

    n = Network.from_json(d)

n.print()
# import networkx as nx
# import matplotlib.pyplot as plt

# m = n.get_number_nodes()
# G = nx.DiGraph() 
# G.add_nodes_from(np.arange(m))

# for i in range(m):
#     for j in range(m):
#         if n.connections[i, j] > 0:
#             print('edge: {} - {}'.format(i, j))
#             G.add_weighted_edges_from([(i, j, n.connections[i, j])])


# nx.draw_networkx(G, arrows=True, with_labels=True)

# plt.legend(handles=[n.nodes[i].name for i in range(m)])
# plt.show()

#wave = Wave(n.nodes[5], 2)
#n.applyWave(wave)
#wave = Wave(n.nodes[3], 2.5)
#n.applyWave(wave)

for i in range(5):
    n.perform_step()
    n.print()

print('finished')