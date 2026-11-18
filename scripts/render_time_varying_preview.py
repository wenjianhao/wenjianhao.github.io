"""Replot the recorded gamma=6 markers from gamma-comparison.mp4, not a new simulation."""
import argparse
import subprocess
from collections import deque

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def recorded_states(ffmpeg, source):
    # Right-hand phase plot in the original 1976x1170 export. Grid crossings
    # in the crop calibrate x1=0 at 94 px, x2=0 at 444 px.
    w, h = 892, 576
    with subprocess.Popen([ffmpeg, '-v', 'error', '-i', source, '-an', '-vf',
                           f'crop={w}:{h}:1080:36', '-pix_fmt', 'rgb24',
                           '-f', 'rawvideo', '-'], stdout=subprocess.PIPE) as p:
        while raw := p.stdout.read(w*h*3):
            rgb = np.frombuffer(raw, np.uint8).reshape(h, w, 3)
            r, g, b = rgb.transpose(2, 0, 1)
            markers = [(r > 155) & (g < 70) & (b < 70),
                       (r < 52) & (g > 70) & (g < 142) & (b > 140)]
            pair = []
            for mask in markers:
                mask[:41, :365] = False  # Exclude the source legend.
                y, x = np.where(mask)
                # The current marker has the densest cluster of saturated pixels.
                if not len(x):
                    raise ValueError('Missing marker')
                dense = ((abs(x[:,None]-x) < 5) & (abs(y[:,None]-y) < 5)).sum(axis=1).argmax()
                near = (abs(x-x[dense]) < 11) & (abs(y-y[dense]) < 11)
                if near.sum() < 35:
                    raise ValueError('Cannot locate a reliable current marker')
                cx, cy = np.median(x[near]), np.median(y[near])
                pair.append(((cx-94)/207.5, (444-cy)/111.5))
            yield pair
        if p.wait():
            raise RuntimeError('Source decoding failed')


def render(ffmpeg, source, output, poster):
    w, h = 720, 620
    ink, actual, forecast = '#172a39', '#000000', '#ad491e'
    large, small = (ImageFont.load_default(size=n) for n in (35, 25))
    try:
        title_font, title_stroke = ImageFont.truetype('Arial Bold.ttf', 25), 0
    except OSError:
        title_font, title_stroke = small, 1
    history = deque(maxlen=34)
    states = list(recorded_states(ffmpeg, source))
    # L2 error from video-extracted markers, not the original numerical dataset.
    errors = [float(np.linalg.norm(np.subtract(pair[0], pair[1]))) for pair in states]
    if not errors or not np.isfinite(errors).all():
        raise ValueError('Missing or invalid recorded state errors')
    error_limit = max(0.1, float(np.ceil(max(errors) * 10) / 10))
    error_history = deque(maxlen=34)
    gif = str(output).lower().endswith('.gif')
    codec = (['-filter_complex', 'fps=12,scale=480:-1:flags=lanczos,split[a][b];'
              '[a]palettegen[p];[b][p]paletteuse=dither=none', '-loop', '0']
             if gif else ['-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart'])
    with subprocess.Popen([ffmpeg, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt',
                           'rgb24', '-s', f'{w}x{h}', '-r', '24', '-i', '-', '-an',
                           *codec, output], stdin=subprocess.PIPE) as enc:
        for frame, pair in enumerate(states):
            history.append(pair)
            error_history.append(errors[frame])
            img = Image.new('RGB', (w, h), '#ffffff' if gif else '#fbfaf6')
            draw = ImageDraw.Draw(img)
            # Two state panels together occupy twice the error panel's height.
            # All panels use the same rolling simulation-step window.
            def time_x(i):
                return 82 + i * 613 / 33
            draw.text((82, 10), 'Fast time-varying system', fill=ink, font=title_font,
                      stroke_width=title_stroke, stroke_fill=ink)
            draw.text((681, 54), f'Step: {101+frame}', anchor='ra', fill=ink, font=small)
            draw.line((98, 69, 131, 69), fill=actual, width=5)
            draw.text((142, 54), 'True state', fill=ink, font=small)
            draw.ellipse((315, 63, 327, 75), outline=forecast, width=3)
            draw.text((340, 54), 'Predicted state', fill=ink, font=small)
            for dim, top in enumerate((100, 262)):
                bottom = top + 132
                def state_y(value):
                    return bottom - (value + 1) / 6.5 * 132
                for value in (0, 2, 4):
                    y = state_y(value)
                    draw.line((82, y, 695, y), fill='#d7dfde', width=1)
                    draw.text((72, y), str(value), anchor='rm', fill=ink, font=small)
                for i in (0, 11, 22, 33):
                    x = time_x(i)
                    draw.line((x, top, x, bottom), fill='#edf0f0', width=1)
                draw.rectangle((82, top, 695, bottom), outline='#7c908e', width=1)
                draw.text((25, top + 54), ('x1', 'x2')[dim], fill=ink, font=small)
                pts = [(time_x(i), state_y(p[0][dim])) for i, p in enumerate(history)]
                if len(pts) > 1:
                    draw.line(pts, fill=actual, width=5)
                for i, p in enumerate(history):
                    x, y = time_x(i), state_y(p[1][dim])
                    draw.ellipse((x-5, y-5, x+5, y+5), outline=forecast, width=3)
            error_top, error_bottom = 424, 556
            # Leave headroom for the in-panel label without covering the error curve.
            error_scale = error_limit * 1.35
            for value in (0, error_limit / 2, error_limit):
                y = error_bottom - value / error_scale * (error_bottom - error_top)
                draw.line((82, y, 695, y), fill='#d7dfde', width=1)
                draw.text((72, y), f'{value:g}', anchor='rm', fill=ink, font=small)
            start_step = 101 + frame - len(history) + 1
            for i in (0, 11, 22, 33):
                x = time_x(i)
                draw.line((x, error_top, x, error_bottom), fill='#edf0f0', width=1)
                draw.text((x, 562), str(start_step + i), anchor='lt' if i == 0 else 'mt',
                          fill=ink, font=small)
            draw.rectangle((82, error_top, 695, error_bottom), outline='#7c908e', width=1)
            error_pts = [(time_x(i), error_bottom - value / error_scale *
                          (error_bottom - error_top)) for i, value in enumerate(error_history)]
            if len(error_pts) > 1:
                draw.line(error_pts, fill=actual, width=3)
            x, y = error_pts[-1]
            draw.ellipse((x-3, y-3, x+3, y+3), fill=actual)
            draw.text((96, error_top + 8), 'Prediction error', fill='#000000', font=small)
            draw.text((388, 590), 'Time step', anchor='mt', fill=ink, font=small)
            if frame == 72:
                img.save(poster, quality=90)
            enc.stdin.write(img.tobytes())
        enc.stdin.close()
        if enc.wait():
            raise RuntimeError('Preview encoding failed')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'output', 'poster'):
        cli.add_argument(name)
    cli.add_argument('--ffmpeg', default='ffmpeg')
    args = cli.parse_args()
    render(args.ffmpeg, args.source, args.output, args.poster)
