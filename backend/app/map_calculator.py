import heapq
from app.schemas.core import TrainStationWithConnectionSchema
from typing import List


def shortest_path(graph: List[TrainStationWithConnectionSchema], start: str, end: str):
    node_map = {node.id: node for node in graph}
    distances = {node.id: float("inf") for node in graph}
    distances[start] = 0
    pq = [(0, None, start)]
    previous_nodes = {node.id: None for node in graph}
    tracked_shortest_path = []

    while pq:
        current_distance, current_line, current_node_id = heapq.heappop(pq)

        if current_distance > distances[current_node_id]:
            continue

        current_node = node_map.get(current_node_id)

        if current_node is None:
            continue

        if current_node_id == end:
            while previous_nodes[current_node.id]:
                tracked_shortest_path.append(current_node)
                current_node = previous_nodes[current_node.id]
            tracked_shortest_path.append(node_map[start])
            tracked_shortest_path.reverse()

            return distances[end], tracked_shortest_path

        for station in current_node.connecting_stations or []:
            neighbor_id = station.connecting_id
            neighbor_distance = current_distance + station.distance
            neighbor_line = current_line

            if (
                current_line is not None
                and current_line != station.line
                and (current_node_id != start or station.line != end)
            ):
                # add transit and waiting time if line changes
                if station.transit_time is not None:
                    neighbor_distance += station.transit_time
                if current_node_id != start:
                    neighbor_distance += station.waiting_time

            if current_line is None or current_line != station.line:
                # update neighbor_line if line changes
                neighbor_line = station.line

            if neighbor_distance < distances[neighbor_id]:
                distances[neighbor_id] = neighbor_distance
                previous_nodes[neighbor_id] = current_node  # type: ignore
                heapq.heappush(pq, (neighbor_distance, neighbor_line, neighbor_id))

    return 0, []
