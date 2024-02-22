import json
from flet import Paint, colors, TextStyle, alignment, TextAlign

from flet.canvas import *


class GraphFile:
    _canvas: Canvas

    def __init__(self, canvas_control: Canvas):
        self._canvas = canvas_control

    # returning (points, lines)
    def _transform_to_coordinates(self) -> tuple[list, list]:
        return (
            [(point.x, point.y) for point in self._canvas.shapes if isinstance(point, Circle)],
            [((line.x1, line.y1), (line.x2, line.y2)) for line in self._canvas.shapes if isinstance(line, Line)]
        )

    def _transform_to_controls(self, points: list[tuple], lines: list[tuple]) -> tuple:
        return (
            [
                Circle(
                    x=point[0],
                    y=point[1],
                    paint=Paint(
                        color=colors.BLACK,
                        stroke_width=1
                    ),
                    radius=5
                ) for point in points
            ],
            [
                Line(
                    x1=line[0][0],
                    y1=line[0][1],
                    x2=line[1][0],
                    y2=line[1][1],
                    paint=Paint(
                        color=colors.BLACK,
                        stroke_width=1
                    ),
                ) for line in lines
            ]
        )

    def export_file(self, filename: str):
        transformed_canvas = self._transform_to_coordinates()
        with open(filename, mode="w+", encoding='utf-8') as file:
            file.write(
                json.dumps(
                    {
                        'image': self._canvas.content.content.image_src,
                        'coordinates': {
                            'points': transformed_canvas[0],
                            'lines': transformed_canvas[1]
                        }
                    }
                )
            )

    def import_file(self, filename: str):
        shape_list = []
        with open(filename, mode='r', encoding='utf-8') as file:
            data = json.loads(file.read())
            transformed_coordinates = self._transform_to_controls(
                data['coordinates']['points'],
                data['coordinates']['lines'],
            )
            if transformed_coordinates:
                self._canvas.content.content.image_src = data['image']
                for index, point, line in zip(range(len(transformed_coordinates[0])), *transformed_coordinates):
                    point.data = index
                    shape_list += [
                        line,
                        point,
                        Text(
                            x=point.x,
                            y=point.y + 20,
                            text=f"رأس {index + 1}",
                            style=TextStyle(
                                color=colors.RED,
                                font_family='yekanbakh.regular'
                            ),
                            alignment=alignment.center,
                            text_align=TextAlign.CENTER,
                            data=index
                        )
                    ]

                self._canvas.shapes = shape_list
