import vapoursynth as vs
core = vs.core
# 4 s, 1280x720, 24 fps synthetic clip; text title + sharpen + levels.
base = core.std.BlankClip(width=1280, height=720, format=vs.YUV420P8, length=96, fpsnum=24, fpsden=1, color=[30, 128, 128])
titled = core.text.Text(base, "VAPOURSYNTH", alignment=5, scale=4.0)
sharp = core.std.Convolution(titled, matrix=[0, -1, 0, -1, 5, -1, 0, -1, 0])
graded = core.std.Levels(sharp, min_in=16, max_in=235, min_out=0, max_out=255)
graded.set_output()
