#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass


class Paint:
    def __init__(self, color: str = "red"):
        self.color: str = color


@dataclass
class InterpolateColor:
    to_number_name: str
    limits: [float]

    def color(self):
        return [
            "interpolate",
            ["linear"],
            ["to-number", ["get", self.to_number_name]],
            self.limits[0],
            "green",
            self.limits[1],
            "orange",
            self.limits[2],
            "red"
        ]


class LinePaint(Paint):
    def __init__(self, line_color=None, line_width: int = 2):
        super().__init__(line_color)
        if line_color is None:
            line_color = "red"
        self.paint = {
            "line-color": line_color,
            "line-width": line_width
        }


class CirclePaint(Paint):
    def __init__(self, color: str = 'blue', circle_stroke_color: str = 'black',
                 circle_stroke_width: int = 1, circle_radius: int = 14):
        super().__init__(color)
        self.paint = {"circle-radius": circle_radius, "circle-color": color,
                      "circle-stroke-color": circle_stroke_color,
                      "circle-stroke-width": circle_stroke_width, }


class SymbolPaint(Paint):
    def __init__(self, color: str = 'white'):
        super().__init__(color)
        self.paint = {"text-color": color}


class Layout:

    def __init__(self, text_field, text_font=None, text_size: int = 14, symbol_placement: str = "point"):
        if text_font is None:
            text_font = ["DIN Offc Pro Medium", "Arial Unicode MS Bold"]
        self.text_field: [str] = text_field
        self.text_font: [str] = text_font
        self.text_size: int = text_size
        self.symbol_placement: str = symbol_placement
        self.layout = self.layout()

    def layout(self):
        return {
            "text-field": ["format", ["get", self.text_field]],
            "text-font": self.text_font,
            "text-size": self.text_size,
            "symbol-placement": self.symbol_placement
        }


class BasicStyle:

    def __init__(self, style_id: str, style_type: str, name: str, paint: {} = None,
                 style_filter: [str] = None):
        self.style_id = style_id
        self.name = name
        self.style_type = style_type
        self.style_filter = style_filter
        self.paint = paint
        self.style: {} = {}

    def write_json_file(self, filename: str):
        f = open(filename, "w")
        f.write(str(self.style))
        f.close()

    def validate_style(self):
        if self.style_type not in ["line", "circle"]:
            raise Exception(f'Style type not valid for style: {self.style_id}')
        elif self.style_type == "line":
            if not isinstance(self.paint, LinePaint):
                raise Exception(
                    f'Style paint {self.paint} is not a valid paint for type: {self.style_type}  '
                    f'in style: {self.style_id}')
        elif self.style_type == "circle":
            if not isinstance(self.paint, CirclePaint):
                raise Exception(
                    f'Style paint {self.paint} is not a valid paint for type: {self.style_type}  '
                    f'in style: {self.style_id}')
        else:
            return True


class CircleStyle(BasicStyle):
    def __init__(self, style_id: str, name: str = '', paint=None, style_filter: [str] = None):
        super().__init__(style_id, style_type='circle', name=name, paint=paint, style_filter=style_filter)
        if self.paint is None:
            paint = CirclePaint().paint
        if self.style_filter is None:
            self.style: {} = {"id": style_id, "name": name, "type": self.style_type, "paint": paint}
        else:
            self.style: {} = {"id": style_id, "name": name, "type": self.style_type, "paint": paint,
                              "filter": self.style_filter}


class LineStyle(BasicStyle):
    def __init__(self, style_id: str, name: str = '', paint=None,
                 style_filter: [str] = None):
        super().__init__(style_id, style_type='line', name=name, paint=paint, style_filter=style_filter)
        if self.paint is None:
            self.paint = LinePaint().paint
        if self.style_filter is None:
            self.style: {} = {"id": self.style_id, "name": self.name, "type": self.style_type, "paint": self.paint}
        else:
            self.style: {} = {"id": self.style_id, "name": self.name, "type": self.style_type, "paint": self.paint,
                              "filter": self.style_filter}


class SymbolStyle(BasicStyle):
    def __init__(self, style_id: str, name: str = '', paint=None, style_filter: [str] = None,
                 minzoom: int = 12, layout=Layout(text_field="parameter").layout):
        super().__init__(style_id, style_type='symbol', name=name, paint=paint, style_filter=style_filter)
        self.minzoom = minzoom
        self.layout = layout
        if self.paint is None:
            self.paint = {"text-color": "white"}
        if self.style_filter is None:
            self.style: {} = {"id": self.style_id, "name": self.name, "type": self.style_type, "paint": self.paint,
                              "minzoom": self.minzoom, "layout": self.layout}
        else:
            self.style: {} = {"id": self.style_id, "name": self.name, "type": self.style_type, "paint": self.paint,
                              "minzoom": self.minzoom,
                              "filter": self.style_filter, "layout": self.layout}


def test():
    circle_style = CircleStyle(style_id='lines1')
    print(circle_style.style)
    ls = LineStyle(style_id='lines')
    print(ls.style)
    ss = SymbolStyle(style_id='parameter', layout=Layout(text_field="parameter",
                                                         text_size=20, symbol_placement='line-center').layout,
                     paint=SymbolPaint(color="black").paint)
    print(ss.style)
    ss.write_json_file(filename="test_style.json")


if __name__ == '__main__':
    test()
