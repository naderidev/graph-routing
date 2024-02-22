import time

from flet import *


class StartView(View):
    def __init__(self):
        super().__init__(
            route='/start',
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
            spacing=30
        )

    def _build(self):
        super()._build()
        self.controls = self.body()

    def body(self) -> list[Control]:
        return [
            Row(
                [
                    Container(
                        image_src='https://avatars.githubusercontent.com/u/48906337?v=4',
                        width=60,
                        height=60,
                        image_fit=ImageFit.COVER,
                        border_radius=25,
                        border=border.all(
                            width=1,
                            color=colors.BLUE_ACCENT_700
                        ),
                        on_click=lambda e: e.page.launch_url('https://github.com/naderidev/')
                    ),
                    Column(
                        [
                            Text(
                                value='پروژه  مسیریابی در گراف',
                                style=TextStyle(
                                    font_family='yekanbakh.fat',
                                    size=30
                                )
                            ),
                            Text(
                                value='طراحی و توسعه توسط: محمدرضا نادری',
                                style=TextStyle(
                                    font_family='yekanbakh.regular',
                                    size=15
                                )
                            )
                        ],
                        spacing=3
                    )
                ],
                vertical_alignment=CrossAxisAlignment.START,
                alignment=MainAxisAlignment.CENTER
            ),
            Row(
                [
                    FilledTonalButton(
                        text='ساخت گراف جدید',
                        style=ButtonStyle(
                            shape=RoundedRectangleBorder(radius=15),
                            color=colors.WHITE,
                            bgcolor=colors.GREEN_ACCENT_700
                        ),
                        icon=icons.DRAW_ROUNDED,
                        adaptive=True,
                        on_click=lambda e: e.page.go("/draw")
                    ),
                    FilledTonalButton(
                        text='بازکردن گراف',
                        style=ButtonStyle(
                            shape=RoundedRectangleBorder(radius=15),
                            color=colors.WHITE,
                            bgcolor=colors.BLUE_ACCENT_700
                        ),
                        icon=icons.FILE_OPEN,
                        adaptive=True,
                        on_click=self._open_file_button
                    )
                ],
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER
            ),

        ]

    def _open_file_button(self, e):
        fp = FilePicker(
            on_result=self._open_file
        )
        self.page.overlay.append(fp)
        self.page.update()
        fp.pick_files(
            dialog_title='درون ریزی فایل',
            allowed_extensions=['ngraph']
        )

    def _open_file(self, e: FilePickerResultEvent):
        if e.files:
            self.page.import_file_path = e.files[0].path
            self.page.go('/draw')
