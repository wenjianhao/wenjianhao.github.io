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
    w, h = 720, 520
    ink, actual, forecast = '#172a39', '#136a78', '#ad491e'
    large, small = (ImageFont.load_default(size=n) for n in (35, 25))
    history = deque(maxlen=34)
    with subprocess.Popen([ffmpeg, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt',
                           'rgb24', '-s', f'{w}x{h}', '-r', '24', '-i', '-', '-an',
                           '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p',
                           '-movflags', '+faststart', output], stdin=subprocess.PIPE) as enc:
        for frame, pair in enumerate(recorded_states(ffmpeg, source)):
            history.append(pair)
            img = Image.new('RGB', (w, h), '#fbfaf6')
            draw = ImageDraw.Draw(img)
            draw.text((22, 15), 'One-step prediction', fill=ink, font=large)
            draw.line((26, 79, 69, 79), fill=actual, width=7)
            draw.text((82, 62), 'True state', fill=ink, font=small)
            draw.ellipse((228, 72, 242, 86), outline=forecast, width=3)
            draw.text((255, 62), 'Prediction from the proposed method', fill=ink, font=small)
            for dim, top in enumerate((112, 286)):
                bottom = top + 147
                draw.text((19, top+51), ('x1', 'x2')[dim], fill=ink, font=large)
                for value in (0, 1, 2, 3):
                    y = bottom - (value+0.75)*33
                    draw.line((82,y,695,y), fill='#d7dfde', width=1)
                def coords(i, v):
                    return (82 + i*18.3, bottom - (v+0.75)*33)
                pts = [coords(i, p[0][dim]) for i,p in enumerate(history)]
                if len(pts) > 1:
                    draw.line(pts, fill=actual, width=5)
                for i, p in enumerate(history):
                    x, y = coords(i, p[1][dim])
                    draw.ellipse((x-5,y-5,x+5,y+5), outline=forecast, width=3)
            draw.line((82,449,695,449), fill='#7c908e', width=2)
            draw.text((82,464), 'Simulation step', fill=ink, font=small)
            # First source frame is labeled step 101 (frame 72 is step 173).
            draw.text((690,464), str(101+frame), anchor='rt', fill=ink, font=small)
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
