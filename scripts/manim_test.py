from manim import *

class VideoLabIntro(Scene):
    def construct(self):
        title = Text("VIDEO LAB", font_size=72, color=GOLD)
        subtitle = Text("Motion graphics from code", font_size=36, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.5)
        circle = Circle(radius=2.2, color=BLUE, stroke_width=6)
        square = Square(side_length=3.2, color=GREEN, stroke_width=6)
        self.play(Create(circle), FadeIn(title), run_time=1.5)
        self.play(Transform(circle, square), FadeIn(subtitle), run_time=1.5)
        self.play(circle.animate.scale(0.6).shift(UP * 0.5), title.animate.shift(DOWN * 0.3), run_time=1)
        self.wait(1)
