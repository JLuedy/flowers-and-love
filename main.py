
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Triangle
from kivy.graphics import Rectangle, Mesh
from kivy.uix.popup import Popup
from math import sin, cos, pi


COLORS = {
    "Pink": (1, 0.25, 0.58, 1),
    "Purple": (0.55, 0.25, 0.9, 1),
    "Red": (0.95, 0.08, 0.18, 1),
    "Blue": (0.1, 0.45, 1, 1),
    "Yellow": (1, 0.75, 0.05, 1),
    "Orange": (1, 0.38, 0.05, 1),
    "Green": (0.1, 0.65, 0.25, 1),
    "White": (1, 1, 1, 1),
}


class Drawing(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flower1 = COLORS["Pink"]
        self.flower2 = COLORS["Purple"]
        self.heart = COLORS["Red"]
        self.center = COLORS["Yellow"]
        self.stem = COLORS["Green"]
        self.bind(pos=self.draw, size=self.draw)

    def draw(self, *args):
        self.canvas.clear()

        with self.canvas:
            Color(1, 0.97, 0.94, 1)
            Rectangle(pos=self.pos, size=self.size)

            w, h = self.size
            ox, oy = self.pos
            scale = max(0.1, min(w / 340, h / 230))

            def point(x, y):
                return ox + w / 2 + x * scale, oy + h / 2 + y * scale

            def line(points, color, width=3):
                Color(*color)
                Line(
                    points=[v for p in points for v in point(*p)],
                    width=width * scale,
                    cap="round",
                    joint="round",
                )

            def flower(x, petal_color):
                line([(x, -65), (x, 5)], self.stem, 4)

                for direction in [-1, 1]:
                    a = point(x, -35)
                    b = point(x + direction * 22, -20)
                    c = point(x + direction * 17, -43)
                    Color(*self.stem)
                    Triangle(points=[*a, *b, *c])

                cx, cy = point(x, 15)
                radius = 20 * scale

                for i in range(8):
                    angle = i * 2 * pi / 8
                    px = cx + cos(angle) * 17 * scale
                    py = cy + sin(angle) * 17 * scale
                    Color(*petal_color)
                    Ellipse(
                        pos=(px-radius/2, py-radius/2),
                        size=(radius, radius),
                    )

                Color(*self.center)
                r = 8 * scale
                Ellipse(pos=(cx-r, cy-r), size=(2*r, 2*r))

            flower(-100, self.flower1)
            flower(100, self.flower2)

            # Draw a filled heart using triangle geometry.
            cx, cy = point(0, -5)
            heart_points = []

            for i in range(101):
                t = 2 * pi * i / 100
                x = 16 * sin(t) ** 3
                y = (
                    13 * cos(t)
                    - 5 * cos(2*t)
                    - 2 * cos(3*t)
                    - cos(4*t)
                )
                heart_points.append((cx + x * scale,
                                     cy + y * scale))

            vertices = []
            for x, y in heart_points:
                vertices.extend([x, y, 0, 0, 1, 1])

            indices = []
            for i in range(1, 100):
                indices.extend([0, i, i + 1])

            Color(*self.heart)
            Mesh(vertices=vertices, indices=indices,
                 mode="triangle_fan")


class FlowersApp(App):
    def build(self):
        self.title = "Flowers & Love"

        root = BoxLayout(
            orientation="vertical",
            padding=8,
            spacing=6,
        )

        root.add_widget(Label(
            text="Flowers & Love",
            color=(0.65, 0.15, 0.4, 1),
            font_size="26sp",
            size_hint_y=None,
            height=45,
        ))

        self.picture = Drawing()
        root.add_widget(self.picture)

        self.selected = {
            "First Flower": "Pink",
            "Second Flower": "Purple",
            "Heart": "Red",
            "Centers": "Yellow",
            "Stems": "Green",
        }

        choices = GridLayout(
            cols=2,
            spacing=5,
            size_hint_y=None,
            height=180,
        )

        for part, color in self.selected.items():
            btn = Button(text=f"{part}: {color}")
            btn.bind(on_release=lambda b, p=part:
                     self.choose_color(p))
            choices.add_widget(btn)

        root.add_widget(choices)

        draw_btn = Button(
            text="Draw My Picture",
            size_hint_y=None,
            height=50,
            background_normal="",
            background_color=(0.85, 0.2, 0.42, 1),
        )
        draw_btn.bind(on_release=self.update_picture)
        root.add_widget(draw_btn)

        return root

    def choose_color(self, part):
        layout = GridLayout(cols=2, spacing=5, padding=8)
        popup = Popup(
            title=f"Choose {part} Color",
            content=layout,
            size_hint=(0.85, 0.65),
        )

        for name, color in COLORS.items():
            btn = Button(
                text=name,
                background_normal="",
                background_color=color,
            )
            btn.bind(on_release=lambda b, n=name:
                     self.set_color(part, n, popup))
            layout.add_widget(btn)

        popup.open()

    def set_color(self, part, name, popup):
        self.selected[part] = name
        popup.dismiss()
        self.update_picture()

    def update_picture(self, *args):
        self.picture.flower1 = COLORS[self.selected["First Flower"]]
        self.picture.flower2 = COLORS[self.selected["Second Flower"]]
        self.picture.heart = COLORS[self.selected["Heart"]]
        self.picture.center = COLORS[self.selected["Centers"]]
        self.picture.stem = COLORS[self.selected["Stems"]]
        self.picture.draw()


if __name__ == "__main__":
    FlowersApp().run()

