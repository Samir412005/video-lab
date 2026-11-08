from manim import *

# 10s Algeria video — closing title card (2 s exact by construction).
class AlgeriaTitle(Scene):
    def construct(self):
        title = ImageMobject("scripts/titles10/title1.png").scale(1.0)
        subtitle = ImageMobject("scripts/titles10/title2.png").scale(0.9)
        subtitle.next_to(title, DOWN, buff=0.4)
        sun = Circle(radius=0.6, color=GOLD, fill_opacity=1, stroke_width=0)
        sun.next_to(subtitle, DOWN, buff=0.6)
        self.play(FadeIn(title), run_time=0.7)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.play(GrowFromCenter(sun), run_time=0.8)
