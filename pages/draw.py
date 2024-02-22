from flet import *
import flet.canvas as cv
from core.file import GraphFile


class DrawView(View):
    __canvas: Ref[cv.Canvas] = Ref[cv.Canvas]()
    __current_line: Ref[cv.Line] = Ref[cv.Line]()
    __current_local: tuple = 0, 0
    __point_counter: int = 1

    def __init__(self):
        super().__init__(
            route='/draw',
            floating_action_button=FloatingActionButton(
                icon=icons.CHECK,
                bgcolor=colors.GREEN_ACCENT_700,
                mini=True,
                on_click=self._go_routing
            ),
            floating_action_button_location=FloatingActionButtonLocation.START_FLOAT
        )

    def _build(self):
        super()._build()
        if not hasattr(self.page, 'graph'):
            self.page.graph = None

        self.controls = self.body()
        self.page.overlay.clear()
        if hasattr(self.page, 'import_file_path') and not self.page.graph:
            graph = GraphFile(self.__canvas.current)
            graph.import_file(self.page.import_file_path)

        if self.page.graph:
            self.__canvas.current.shapes = self.page.graph['shapes']
            self.__canvas.current.content.content.image_src = self.page.graph['image']

        if self._get_points():
            self.__point_counter = len(self._get_points()) + 1

    def body(self) -> list[Control]:
        return [
            Stack(
                [
                    cv.Canvas(
                        expand=True,
                        shapes=[],
                        content=GestureDetector(
                            content=Container(
                                image_src='',
                                image_fit=ImageFit.CONTAIN,
                                opacity=0.5,
                                border_radius=20,
                                bgcolor=colors.BLACK12
                            ),
                            on_pan_start=self._on_pan_start,
                            on_pan_update=self._on_pan_update,
                            on_pan_end=self._on_pan_end
                        ),
                        ref=self.__canvas
                    ),
                    Column(
                        [
                            Text(
                                value="طراحی گراف جدید",
                                font_family='yekanbakh.fat',
                                size=30,
                            ),
                            Text(
                                value="در این بخش یک گراف جدید طراحی کنید و پس از اتمام طراحی بر روی تیک کلیک کنید.",
                                font_family='yekanbakh.regular',
                                size=13,
                            ),
                        ],
                        top=20,
                        right=20,
                        alignment=MainAxisAlignment.START,
                        horizontal_alignment=CrossAxisAlignment.START,
                        spacing=0
                    ),
                    Row(
                        [
                            IconButton(
                                tooltip='واگرد',
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=15),
                                    color=colors.WHITE,
                                    bgcolor=colors.BLACK
                                ),
                                icon=icons.UNDO_ROUNDED,
                                scale=0.85,
                                on_click=self._undo_on_click

                            ),
                            IconButton(
                                tooltip='پاک کردن همه',
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=15),
                                    color=colors.WHITE,
                                    bgcolor=colors.BLACK
                                ),
                                icon=icons.CLEAR_ALL,
                                scale=0.85,
                                on_click=self._clear_all

                            ),
                            IconButton(
                                tooltip='خروجی',
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=15),
                                    color=colors.WHITE,
                                    bgcolor=colors.BLACK
                                ),
                                icon=icons.DRIVE_FILE_MOVE,
                                scale=0.85,
                                on_click=self._export_file_button

                            ),
                            IconButton(
                                tooltip='تغییر عکس پست زمینه',
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=15),
                                    color=colors.WHITE,
                                    bgcolor=colors.BLACK
                                ),
                                icon=icons.PHOTO_ROUNDED,
                                scale=0.85,
                                on_click=self._set_background_button

                            ),
                        ],
                        spacing=0,
                        top=10,
                        left=10,
                        right=0,
                        alignment=MainAxisAlignment.END,
                        vertical_alignment=CrossAxisAlignment.END,
                    ),
                ],
                expand=True
            )

        ]

    def _clear_all(self, e):
        self.__canvas.current.shapes.clear()
        self.__canvas.current.update()

    def _set_background_button(self, e):
        fp = FilePicker(
            on_result=self._set_background
        )
        self.page.overlay.append(fp)
        self.page.update()
        fp.pick_files(
            dialog_title='عکس پست زمینه',
            file_type=FilePickerFileType.IMAGE
        )

    def _export_file_button(self, e):
        fp = FilePicker(
            on_result=self._export_file
        )
        self.page.overlay.append(fp)
        self.page.update()
        fp.save_file(
            dialog_title='ذخیره خروجی',
            allowed_extensions=['ngraph']
        )

    def _export_file(self, e: FilePickerResultEvent):
        if e.path:
            graph = GraphFile(self.__canvas.current)
            graph.export_file(e.path + ".ngraph")

    def _set_background(self, e: FilePickerResultEvent):
        if e.files:
            self.__canvas.current.content.content.image_src = e.files[0].path
            self.__canvas.current.update()

    def _undo_on_click(self, e):
        if self.__canvas.current.shapes:
            last_shape = self.__canvas.current.shapes[-1]
            if isinstance(last_shape, cv.Line):
                self.__canvas.current.shapes.pop(-1)

            elif isinstance(last_shape, cv.Text):
                self.__canvas.current.shapes = self.__canvas.current.shapes[:-3]

        self.__canvas.current.update()

    def _on_pan_start(self, e: DragStartEvent):
        near_point = self._get_near_point((e.local_x, e.local_y))
        self.__current_local = near_point if near_point else (e.local_x, e.local_y)
        self.__canvas.current.shapes.append(
            cv.Line(
                x1=self.__current_local[0],
                y1=self.__current_local[1],
                x2=self.__current_local[0],
                y2=self.__current_local[1],
                paint=Paint(
                    color=colors.BLACK87,
                    stroke_width=1
                ),
                ref=self.__current_line
            )
        )
        self.__canvas.current.update()
        if not near_point:
            self._add_point(self.__current_local)

    def _on_pan_update(self, e: DragUpdateEvent):
        if self.__current_line:
            self.__current_line.current.x2 = e.local_x
            self.__current_line.current.y2 = e.local_y
            self.__current_line.current.update()
            self.__current_local = e.local_x, e.local_y

    def _get_points(self) -> list[cv.Circle]:
        return [
            point for point in self.__canvas.current.shapes if isinstance(point, cv.Circle)
        ]

    def _is_on_point(self, point: tuple, line_local: tuple) -> bool:
        return (line_local[0] - point[0]) ** 2 + (line_local[1] - point[1]) ** 2 <= 64

    def _get_near_point(self, line: tuple) -> tuple | None:
        points = list(map(lambda x: (x.x, x.y), self._get_points()))
        for p in points:
            on_point = self._is_on_point(p, line)
            if on_point:
                return p

        return None

    def _add_point(self, position: tuple):
        self.__canvas.current.shapes += [
            cv.Circle(
                x=position[0],
                y=position[1],
                radius=5,
                paint=Paint(
                    color=colors.BLACK,
                    stroke_width=1
                ),
                data=self.__point_counter
            ),
            cv.Text(
                x=position[0],
                y=position[1] + 20,
                text=f"رأس {self.__point_counter}",
                alignment=alignment.center,
                text_align=TextAlign.CENTER,
                style=TextStyle(
                    color=colors.RED,
                    font_family='yekanbakh.regular'
                ),
                data=self.__point_counter
            )
        ]
        self.__canvas.current.update()
        self.__point_counter += 1

    def _on_pan_end(self, e: DragEndEvent):
        near_point = self._get_near_point(self.__current_local)
        if near_point:
            self.__current_line.current.x2 = near_point[0]
            self.__current_line.current.y2 = near_point[1]
            self.__current_line.current.update()
            self.__current_line = Ref[cv.Line]()

        else:
            self._add_point(self.__current_local)

    def _go_routing(self, e):
        if self.__canvas.current.shapes:
            self.page.graph = {
                'image': self.__canvas.current.content.content.image_src,
                'shapes': self.__canvas.current.shapes
            }
            self.page.go('/routing')
