import numpy as np

from typing import Union
from renderer.data import PlayerInfo
from renderer.render import Renderer
from renderer.base import LayerBase
from renderer.const import RELATION_NORMAL_STR, COLORS_NORMAL
from PIL import Image, ImageDraw, ImageColor


class LayerScoreBase(LayerBase):
    def __init__(self, renderer: Renderer):
        self._renderer = renderer
        self._font = self._renderer.resman.load_font(
            filename="warhelios_bold.ttf", size=28
        )
        self._base = Image.new("RGBA", (760, 50))

    def draw(self, game_time: int, image: Image.Image):
        evt_score = self._renderer.replay_data.events[game_time].evt_score
        base = self._base.copy()

        sc1 = evt_score[0]
        sc2 = evt_score[1]

        per1 = 1 - sc1.score / self._renderer.replay_data.game_win_score
        per2 = 1 - sc2.score / self._renderer.replay_data.game_win_score

        draw = ImageDraw.Draw(base)
        st = f"{sc1.score} : {sc2.score}"
        st_w, st_h = self._font.getsize(st)
        st_h += 5
        draw.text(
            (
                round(base.width / 2 - st_w / 2),
                round(base.height / 2 - st_h / 2),
            ),
            text=st,
            font=self._font,
            fill="white"
        )

        mid = base.width / 2
        space_width = 150
        margin = 5

        x1, y1 = margin, margin
        x2, y2 = mid - space_width / 2, base.height - margin
        draw.rectangle(((x1, y1), (x2, y2)), outline=COLORS_NORMAL[0])
        x3, y3 = mid + space_width / 2, margin
        x4, y4 = base.width - margin, base.height - margin
        draw.rectangle(((x3, y3), (x4, y4)), outline=COLORS_NORMAL[1])
        a1, b1 = margin, margin
        a2, b2 = mid - space_width / 2, base.height - margin
        a1 = margin + (x2 * per1) - (margin * per1)
        draw.rectangle(((a1, b1), (a2, b2)), fill=COLORS_NORMAL[0])
        a3, b3 = mid + space_width / 2, margin
        a4, b4 = base.width - margin, base.height - margin
        a4 = x4 - (base.width / 2 - space_width / 2) * per2 + (margin * per2)
        draw.rectangle(((a3, b3), (a4, b4)), fill=COLORS_NORMAL[1])
        image.paste(base, (40, 0), base)