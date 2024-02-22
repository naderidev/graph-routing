from flet import *

from pages.draw import DrawView
from pages.routing import RoutingView
from pages.start import StartView


class CONFIG:
    page: Page

    # Window Details
    APP_TITLE: str = 'Graph Routing v0.0.1'
    THEME_MODE: str = ThemeMode.LIGHT
    WINDOW_RESIZEABLE = False
    FONTS: dict = {
        # Yehan Bakh
        "yekanbakh.fat": "fonts/yehan_bakh/Fat.ttf",
        "yekanbakh.heavy": "fonts/yehan_bakh/Heavy.ttf",
        "yekanbakh.regular": "fonts/yehan_bakh/Regular.ttf",
    }

    def setup(self):

        # Routing settings
        self.page.on_route_change = self.__on_route_changed
        self.page.views.append(self.views()[0])

        # Window
        self.page.title = self.APP_TITLE
        self.page.theme_mode = self.THEME_MODE
        self.page.window_resizable = self.WINDOW_RESIZEABLE
        self.page.fonts = self.FONTS
        self.page.theme = Theme(
            font_family='yekanbakh.regular'
        )
        self.page.padding = 0
        self.page.rtl = True

    def __on_route_changed(self, e: RouteChangeEvent):
        for _view in self.views():
            if TemplateRoute(e.route).match(_view.route):
                e.page.views.clear()
                e.page.views.append(_view)
                break

    def views(self) -> list[View]:
        return []


class App(CONFIG):
    page: Page

    def __init__(self, page: Page):
        self.page = page
        self.setup()
        self.page.update()

    def views(self) -> list[View]:
        return [
            StartView(),
            DrawView(),
            RoutingView()
        ]


app(
    target=App,
    assets_dir='assets'
)
