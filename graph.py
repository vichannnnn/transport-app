import json
import heapq


def load_graph(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data


# def shortest_path(graph, start, end, path=None):
#     if not path:
#         path = []
#
#     #  append current station onto path so that we traverse
#     path = path + [start]
#
#     # if we reached destination, we just return the entire path
#     if start == end:
#         return path
#
#     # if the station we're at is not in part of the map, ends it
#     if start not in graph.keys():
#         return None
#
#     # we record the current shortest by length
#     shortest = None
#
#     # we go through every possibilities by branching out from adjacent station
#     # e.g. woodlands we go both admiralty and marsiling
#     for node in graph[start]:
#         if node not in path:
#             # does a recursion and continues with our built up path
#             new_path = shortest_path(graph, node, end, path)
#             # if new_path, it means we have already completed a variation of the destination
#             if new_path:
#                 # if there are no recorded shortest or the new_path is the shortest, then replace it
#                 if not shortest or len(new_path) < len(shortest):
#                     shortest = new_path
#     return shortest


def shortest_path(graph, start, end):
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    previous_nodes = {node: None for node in graph}
    tracked_shortest_path = []

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        if current_node == end:
            while previous_nodes[current_node]:
                tracked_shortest_path.append(current_node)
                current_node = previous_nodes[current_node]
            tracked_shortest_path.append(start)
            tracked_shortest_path.reverse()
            return (distances[end], tracked_shortest_path)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return float("inf"), []


graph = load_graph("stations.json")
print(shortest_path(graph, "Woodlands", "Dhoby Ghaut"))

a = {
    "ns1/ew24": ["ns2", "ew23", "ew25"],
    "ns2": ["ns1/ew24", "ns3"],
    "ns3": ["ns2", "ns4/bp1"],
    "ns4/bp1": ["ns3", "ns5", "bp2"],
    "ns5": ["ns4/bp1", "ns6"],
    "ns6": ["ns5", "ns7"],
    "ns7": ["ns6", "ns8"],
    "ns8": ["ns7", "ns9/te2"],
    "ns9/te2": ["ns8", "ns10", "te1", "te3"],
    "ns10": ["ns9/te2", "ns11"],
    "ns11": ["ns10", "ns12"],
    "ns12": ["ns11", "ns13"],
    "ns13": ["ns12", "ns14"],
    "ns14": ["ns13", "ns15"],
    "ns15": ["ns14", "ns16"],
    "ns16": ["ns15", "ns17/cc15"],
    "ns17/cc15": ["ns16", "ns18", "cc14", "cc16"],
    "ns18": ["ns17/cc15", "ns19"],
    "ns19": ["ns18", "ns20"],
    "ns20": ["ns19", "ns21/dt11"],
    "ns21/dt11": ["ns20", "ns22", "dt11"],
    "ns22": ["ns21/dt11", "ns23"],
    "ns23": ["ns24/ne6/cc1", "ns22"],
    "ns24/ne6/cc1": ["ns23", "ns25/ew13", "ne5", "ne7/dt12", "cc2"],
    "ns25/ew13": ["ns24/ne6/cc1", "ew12/dt14", "ns26/ew14"],
    "ns26/ew14": ["ns25/ew13", "ns27/ce2", "ew15"],
    "ns27/ce2": ["ns26/ew14", "ns28", "ce1/dt16"],
    "ns28": ["ns27/ce2"],
    "ew1": ["ew2/dt32"],
    "ew2/dt32": ["ew1", "ew3", "dt31", "dt33"],
    "ew3": ["ew2/dt32", "ew4/cg"],
    "ew4/cg": ["ew3", "ew5", "cg1/dt35"],
    "ew5": ["ew4/cg", "ew6"],
    "ew6": ["ew5", "ew7"],
    "ew7": ["ew6", "ew8/cc9"],
    "ew8/cc9": ["ew7", "cc8", "ew9", "cc10/dt26"],
    "ew9": ["ew8/cc9", "ew10"],
    "ew10": ["ew9", "ew11"],
    "ew11": ["ew10", "ew12/dt14"],
    "ew12/dt14": ["ew11", "ns25/ew13", "dt13", "cc4/dt15"],
    "ew15": ["ew16/ne3", "ns26/ew14"],
    "ew16/ne3": ["ew15", "ew17", "ne1/cc29", "ne4/dt19"],
    "ew17": ["ew16/ne3", "ew18"],
    "ew18": ["ew17", "ew19"],
    "ew19": ["ew18", "ew20"],
    "ew20": ["ew19", "ew21/cc22"],
    "ew21/cc22": ["ew20", "ew22", "cc21", "cc23"],
    "ew22": ["ew21/cc22", "ew23"],
    "ew23": ["ew22", "ns1/ew24"],
    "ew25": ["ns1/ew24", "ew26"],
    "ew26": ["ew25", "ew27"],
    "ew27": ["ew26", "ew28"],
    "ew28": ["ew27", "ew29"],
    "ew29": ["ew28", "ew30"],
    "ew30": ["ew29", "ew31"],
    "ew31": ["ew30", "ew32"],
    "ew32": ["ew31", "ew33"],
    "ew33": ["ew32"],
    "cg1/dt35": ["ew4/cg", "cg2", "dt34"],
    "cg2": ["cg1/dt35"],
    "ne1/cc29": ["ew16/ne3", "cc28"],
    "ne4/dt19": ["ew16/ne3", "ne5", "dt18", "dt20"],
    "ne5": ["ne4/dt19", "ns24/ne6/cc1"],
    "ne7/dt12": ["ns24/ne6/cc1", "ne8", "dt11", "dt13"],
    "ne8": ["ne7/dt12", "ne9"],
    "ne9": ["ne8", "ne10"],
    "ne10": ["ne9", "ne11"],
    "ne11": ["ne10", "ne12/cc13"],
    "ne12/cc13": ["ne11", "ne13", "cc12", "cc14"],
    "ne13": ["ne12/cc13", "ne14"],
    "ne14": ["ne13", "ne15"],
    "ne15": ["ne14", "ne16/stc"],
    "ne16/stc": ["ne15", "ne17/ptc", "se1", "se5", "sw1", "sw8"],
    "ne17/ptc": ["ne16/stc", "pe1", "pe7", "pw1", "pw7"],
    "cc2": ["ns24/ne6/cc1", "cc3"],
    "cc3": ["cc2", "cc4/dt15"],
    "cc4/dt15": ["cc3", "cc5"],
    "cc5": ["cc4/dt15", "cc6"],
    "cc6": ["cc5", "cc7"],
    "cc7": ["cc6", "cc8"],
    "cc8": ["cc7", "ew8/cc9"],
    "cc10/dt26": ["ew8/cc9", "cc11", "dt25", "dt27"],
    "cc11": ["cc10/dt26", "cc12"],
    "cc12": ["cc11", "ne12/cc13"],
    "cc14": ["ne12/cc13", "ns17/cc15"],
    "cc16": ["ns17/cc15", "cc17/te9"],
    "cc17/te9": ["cc16", "cc19/dt9", "te8"],
    "cc19/dt9": ["cc17/te9", "cc20", "dt8", "dt10"],
    "cc20": ["cc19/dt9", "cc21"],
    "cc21": ["cc20", "ew21/cc22"],
    "cc23": ["ew21/cc22", "cc24"],
    "cc24": ["cc23", "cc25"],
    "cc25": ["cc24", "cc26"],
    "cc26": ["cc25", "cc27"],
    "cc27": ["cc26", "cc28"],
    "cc28": ["cc27", "ne1/cc29"],
    "bp6/dt1": ["dt2", "bp5", "bp7", "bp13"],
    "dt2": ["bp6/dt1", "dt3"],
    "dt3": ["dt2", "dt5"],
    "dt5": ["dt3", "dt6"],
    "dt6": ["dt5", "dt7"],
    "dt7": ["dt6", "dt8"],
    "dt8": ["dt7", "cc19/dt9"],
    "dt10": ["cc19/dt9", "ns21/dt11"],
    "dt13": ["ne7/dt12", "ew12/dt14"],
    "ce1/dt16": ["cc4/dt15", "dt17"],
    "dt17": ["ce1/dt16", "dt18"],
    "dt18": ["dt17", "ne4/dt19"],
    "dt20": ["ne4/dt19", "dt21"],
    "dt21": ["dt20", "dt22"],
    "dt22": ["dt21", "dt23"],
    "dt23": ["dt22", "dt24"],
    "dt24": ["dt23", "dt25"],
    "dt25": ["dt24", "cc10/dt26"],
    "dt27": ["cc10/dt26", "dt28"],
    "dt28": ["dt27", "dt29"],
    "dt29": ["dt28", "dt30"],
    "dt30": ["dt29", "dt31"],
    "dt31": ["dt30", "ew2/dt32"],
    "dt33": ["ew2/dt32", "dt34"],
    "dt34": ["dt33", "cg1/dt35"],
    "bp2": ["ns4/bp1", "bp3"],
    "bp3": ["bp2", "bp4"],
    "bp4": ["bp3", "bp5"],
    "bp5": ["bp4", "bp6/dt1", "bp14"],
    "bp7": ["bp6/dt1", "bp8"],
    "bp8": ["bp7", "bp9"],
    "bp9": ["bp8", "bp10"],
    "bp10": ["bp9", "bp11"],
    "bp11": ["bp10", "bp12"],
    "bp12": ["bp11", "bp13"],
    "bp13": ["bp12", "bp6/dt1"],
    "bp14": ["bp5"],
    "se1": ["ne16/stc", "se2"],
    "se2": ["se1", "se3"],
    "se3": ["se2", "se4"],
    "se4": ["se3", "se5"],
    "se5": ["se4", "ne16/stc"],
    "sw1": ["ne16/stc", "sw2"],
    "sw2": ["sw1", "sw3"],
    "sw3": ["sw2", "sw4"],
    "sw4": ["sw3", "sw5"],
    "sw5": ["sw4", "sw6"],
    "sw6": ["sw5", "sw7"],
    "sw7": ["sw6", "sw8"],
    "sw8": ["sw7", "ne16/stc"],
    "pe1": ["ne17/ptc", "pe2"],
    "pe2": ["pe1", "pe3"],
    "pe3": ["pe2", "pe4"],
    "pe4": ["pe3", "pe5"],
    "pe5": ["pe4", "pe6"],
    "pe6": ["pe5", "pe7"],
    "pe7": ["pe6", "ne17/ptc"],
    "pw1": ["ne17/ptc", "pw2"],
    "pw2": ["pw1", "pw3"],
    "pw3": ["pw2", "pw4"],
    "pw4": ["pw3", "pw5"],
    "pw5": ["pw4", "pw6"],
    "pw6": ["pw5", "pw7"],
    "pw7": ["pw6", "ne17/ptc"],
    "te1": ["ns9/te2"],
    "te3": ["ns9/te2", "te4"],
    "te4": ["te3", "te5"],
    "te5": ["te4", "te6"],
    "te6": ["te5", "te7"],
    "te7": ["te6", "te8"],
    "te8": ["te7", "cc17/te9"],
}

new = {}
for key, adjacents in a.items():
    new[key] = {i: 1 for i in adjacents}
print(new)
g1 = load_graph("station.json")
g2 = load_graph("stations.json")

result = {k1: k2 for k1, k2 in zip(g1.keys(), g2.keys())}
print(result)
