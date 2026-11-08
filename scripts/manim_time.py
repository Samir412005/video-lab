from manim import *

# «الوقت» — 60 s Arabic motion-graphics film (Manim scenes).
# Scene durations are exact by construction (sum of run_times + waits):
# TimeClock 13 s, TimeBuild 16 s, TimeGrow 14 s, TimeEnd 12 s.
# With the 5 s Blender opener the film is ~60 s.

class TimeClock(Scene):
    def construct(self):
        title = ImageMobject("scripts/titles/title1.png").scale(0.9).to_edge(UP, buff=0.8)
        face = Circle(radius=2.0, color=WHITE, stroke_width=4)
        hand = Line(face.get_center(), face.get_center() + UP * 1.7, color=GOLD, stroke_width=6)
        self.play(Create(face), run_time=1.5)
        self.play(FadeIn(title), run_time=1)
        self.play(Create(hand), run_time=0.5)
        self.play(Rotate(hand, angle=2 * PI, about_point=face.get_center()), run_time=8)
        self.wait(2)


class TimeBuild(Scene):
    def construct(self):
        title = ImageMobject("scripts/titles/title2.png").scale(0.9).to_edge(UP, buff=0.8)
        bars = VGroup(*[
            Rectangle(width=0.9, height=h, fill_color=c, fill_opacity=0.9, stroke_width=0)
            for h, c in [(1.2, BLUE), (2.0, TEAL), (2.8, GREEN), (2.2, GOLD), (3.2, ORANGE)]
        ]).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1.2)
        sun = Circle(radius=0.7, color=GOLD, fill_opacity=1, stroke_width=0).to_edge(UP, buff=1.5).to_edge(RIGHT, buff=1.0)
        self.play(FadeIn(title), run_time=1)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25, run_time=8))
        self.play(GrowFromCenter(sun), run_time=3)
        self.wait(4)


class TimeGrow(Scene):
    def construct(self):
        title = ImageMobject("scripts/titles/title3.png").scale(0.9).to_edge(UP, buff=0.8)
        axes = Axes(x_range=[0, 5, 1], y_range=[0, 3, 1], x_length=8, y_length=4,
                    axis_config={"color": GREY})
        curve = axes.plot(lambda x: 0.12 * x * x + 0.2 * x, x_range=[0, 5], color=GOLD)
        dot = Dot(color=GOLD).scale(1.5).move_to(axes.c2p(5, 4.0))
        self.play(FadeIn(title), run_time=1)
        self.play(Create(axes), run_time=2)
        self.play(Create(curve), run_time=6)
        self.play(GrowFromCenter(dot), run_time=1)
        self.wait(4)


class TimeEnd(Scene):
    def construct(self):
        title = ImageMobject("scripts/titles/title4.png").scale(0.9).to_edge(UP, buff=1.0)
        sun = Circle(radius=1.0, color=GOLD, fill_opacity=1, stroke_width=0).move_to(UP * 1.5)
        horizon = Line(LEFT * 6, RIGHT * 6, color=GREY, stroke_width=3).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(title), run_time=2)
        self.play(Create(horizon), GrowFromCenter(sun), run_time=2)
        self.play(sun.animate.shift(DOWN * 2.2), run_time=5)
        self.wait(3)
