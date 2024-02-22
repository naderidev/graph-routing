from flet import *
import flet.canvas as cv
from flet_core.dropdown import Option

from core.routing import Routing


class RoutingView(View):
    _canvas: Ref[cv.Canvas] = Ref[cv.Canvas]()
    _origin_input: Ref[Dropdown] = Ref[Dropdown]()
    _destination_input: Ref[Dropdown] = Ref[Dropdown]()
    _current_marked_route: list = []

    def __init__(self):
        super().__init__(
            route='/routing',
            floating_action_button=FloatingActionButton(
                icon=icons.EDIT_ROAD,
                bgcolor=colors.YELLOW_ACCENT_700,
                mini=True,
                on_click=lambda e: e.page.go('/draw')
            ),
            floating_action_button_location=FloatingActionButtonLocation.START_FLOAT,
            drawer=NavigationDrawer(
                controls=[
                    Container(
                        content=Column(
                            [
                                Row(
                                    [
                                        Icon(
                                            name=icons.LOCATION_PIN,
                                            color=colors.BLACK
                                        ),
                                        Text(
                                            value='انتخاب مبدا',
                                            font_family='yekanbakh.heavy',
                                            size=20
                                        )
                                    ],
                                    alignment=MainAxisAlignment.START,
                                    vertical_alignment=CrossAxisAlignment.CENTER
                                ),
                                Dropdown(
                                    options=[],
                                    border_radius=15,
                                    border_color=colors.BLACK45,
                                    border_width=1,
                                    height=40,
                                    content_padding=padding.only(
                                        left=10,
                                        right=10,
                                        top=3,
                                        bottom=3
                                    ),
                                    ref=self._origin_input
                                )
                            ]
                        ),
                        bgcolor=colors.WHITE,
                        border_radius=20,
                        padding=15,
                        margin=10
                    ),
                    Container(
                        content=Column(
                            [
                                Row(
                                    [
                                        Icon(
                                            name=icons.LOCATION_PIN,
                                            color=colors.BLACK
                                        ),
                                        Text(
                                            value='انتخاب مقصد',
                                            font_family='yekanbakh.heavy',
                                            size=20
                                        )
                                    ],
                                    alignment=MainAxisAlignment.START,
                                    vertical_alignment=CrossAxisAlignment.CENTER
                                ),
                                Dropdown(
                                    options=[],
                                    border_radius=15,
                                    border_color=colors.BLACK45,
                                    border_width=1,
                                    height=40,
                                    content_padding=padding.only(
                                        left=10,
                                        right=10,
                                        top=3,
                                        bottom=3
                                    ),
                                    ref=self._destination_input
                                )
                            ]
                        ),
                        bgcolor=colors.WHITE,
                        border_radius=20,
                        padding=15,
                        margin=10
                    ),
                    Container(
                        content=FilledTonalButton(
                            text='مسیریابی',
                            style=ButtonStyle(
                                shape=RoundedRectangleBorder(radius=15),
                                color=colors.WHITE,
                                bgcolor=colors.BLUE_ACCENT_700
                            ),
                            icon=icons.ROUTE,
                            adaptive=True,
                            on_click=self._routing_button
                        ),
                        margin=10
                    )
                ],
                bgcolor=colors.WHITE,
                shadow_color=colors.WHITE,
                indicator_color=colors.WHITE,
            )
        )

    def _build(self):
        super()._build()
        self.controls = self.body()
        self._origin_input.current.options = [
            Option(
                text=t.text,
                key=t.data,
            ) for t in list(
                filter(
                    lambda x: isinstance(x, cv.Text),
                    self.page.graph['shapes']
                )
            )
        ]
        self._destination_input.current.options = self._origin_input.current.options = [
            Option(
                text=t.text,
                key=t.data,
            ) for t in list(
                filter(
                    lambda x: isinstance(x, cv.Text),
                    self.page.graph['shapes']
                )
            )
        ]

    def body(self) -> list[Control]:
        return [
            Stack(
                controls=[
                    cv.Canvas(
                        shapes=self.page.graph['shapes'],
                        content=Container(
                            image_src=self.page.graph['image'],
                            image_fit=ImageFit.CONTAIN,
                            opacity=0.5,
                            expand=True,
                            border_radius=20,
                            bgcolor=colors.BLACK12 if not self.page.graph['image'] else colors.TRANSPARENT
                        ),
                        expand=True,
                        ref=self._canvas
                    ),
                    Row(
                        [
                            IconButton(
                                icon=icons.MENU,
                                icon_size=30,
                                icon_color=colors.BLACK,
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=15)
                                ),
                                on_click=self._open_drawer
                            ),
                            Column(
                                [
                                    Text(
                                        value="مسیر یابی در گراف",
                                        font_family='yekanbakh.fat',
                                        size=30,
                                    ),
                                    Text(
                                        value="برای شروع مسیر یابی، منوی کشوی کناری را باز کرده و مبدا و مقصد را انتخاب کنید.",
                                        font_family='yekanbakh.regular',
                                        size=13,
                                    ),
                                ],
                                horizontal_alignment=CrossAxisAlignment.START,
                                spacing=0,
                            ),

                        ],
                        top=20,
                        right=20,
                        alignment=MainAxisAlignment.START,
                        vertical_alignment=CrossAxisAlignment.CENTER
                    )
                ],
                expand=True
            )

        ]

    def _open_drawer(self, e):
        self.drawer.open = True
        self.update()

    def _mark_route(self, shapes: list):
        self._current_marked_route = shapes
        for shape in shapes:
            if shape:
                shape.paint.color = colors.BLUE_ACCENT
                shape.paint.stroke_width = 2

        self._canvas.current.update()

    def _unmark_route(self, shapes: list):
        for shape in shapes:
            if shape:
                shape.paint.color = colors.BLACK
                shape.paint.stroke_width = 1
        self._canvas.current.update()
        self._current_marked_route = []

    def _routing_button(self, e):
        origin = self._origin_input.current.value
        destination = self._destination_input.current.value
        if origin and destination:

            if self._current_marked_route:
                self._unmark_route(self._current_marked_route)

            routing = Routing(self.page.graph['shapes'])
            route = routing.find_shortest_route(
                origin=int(origin),
                destination=int(destination)
            )
            print(route)
            # print(routing.get_all_roads())
            shapes = routing.get_route_shapes(route)
            self._mark_route(shapes)
