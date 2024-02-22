from flet.canvas import *
from collections import deque


class Routing:
    shapes: list = []
    graph: dict = {}

    _lines: list = []
    _points: list = []
    _texts: list = []

    def __init__(self, shapes: list[Circle | Text | Line]):
        self.shapes = shapes
        self._lines, self._texts, self._points = self.get_seperated_shapes()
        self.graph = self.get_all_roads()

    def get_seperated_shapes(self) -> list[
        list[Line],
        list[Text],
        list[Circle]
    ]:
        return [
            list(
                filter(
                    lambda x: isinstance(x, instance),
                    self.shapes
                )
            ) for instance in [Line, Text, Circle]
        ]

    def get_all_roads(self):
        graph: dict = {
            p.data: [] for p in self._points
        }
        for line in self._lines:
            p1, _ = self.get_point_by_coordinates((line.x1, line.y1))
            p2, _ = self.get_point_by_coordinates((line.x2, line.y2))
            p1, p2 = p1.data, p2.data
            graph[p1].append(p2)
            graph[p2].append(p1)

        return graph

    def find_shortest_route(self, origin: int, destination: int):
        queue = deque()
        queue.append((origin, [origin]))
        while queue:
            current_node, path = queue.popleft()
            for neighbor in self.graph[current_node]:
                if neighbor == destination:
                    return path + [neighbor]
                if neighbor not in path:
                    queue.append((neighbor, path + [neighbor]))

        return []

    def get_route_shapes(self, route: list[int]):
        points = self._get_points_by_id(route)
        return self._get_all_lines_between_points(points) + points

    def _get_points_by_id(self, points_id: list[int]) -> list[Circle]:
        return list(
            filter(
                lambda x: x.data in points_id,
                self._points
            )
        )

    def _get_all_lines_between_points(self, points: list) -> list[Line]:
        all_points = sum(map(lambda x: [x.x, x.y], points), [])
        lines = []
        for line in self._lines:
            l = [line.x1, line.x2, line.y1, line.y2]
            if set(l) - set(all_points) == set():
                lines.append(line)

        return lines

    def get_point_by_coordinates(self, coordinates: tuple) -> tuple[Circle, Text] | None:
        point = list(
            filter(
                lambda x: (x[0].x, x[0].y) == coordinates,
                zip(self._points, self._texts)
            )
        )
        return point[0] if point else None
