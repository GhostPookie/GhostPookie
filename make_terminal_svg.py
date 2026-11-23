# Generates terminal.svg: animated fake-terminal for the profile README.
# Pure SVG + CSS (SMIL-free), runs inside GitHub's <img> renderer.
import html

FS = 15            # font size
LH = 26            # line height
CH = 9.0           # approx monospace char width at 15px
PAD_X, TOP, BOT = 20, 46, 20
W = 760

# (prompt?, text, kind) kind: 'cmd' typed char-by-char, 'out' instant reveal
LINES = [
    ('cmd', 'ghost@pookie:~$ whoami', None),
    ('out', 'GhostPookie — software developer', '#c9d1d9'),
    ('cmd', 'ghost@pookie:~$ cat motto.txt', None),
    ('out', 'build things that work; measure whether they do', '#8b949e'),
    ('cmd', 'ghost@pookie:~$ ls /usr/local/stack', None),
    ('out', 'python  numpy  scipy  latex  git  github  linux  bash', '#79c0ff'),
    ('cmd', 'ghost@pookie:~$ uptime', None),
    ('out', '42 days up · load: curiosity · 0 crashes', '#c9d1d9'),
]

T0 = 0.6           # first keystroke delay
CPS = 0.045        # seconds per char
GAP_CMD = 0.55     # pause before typing next command after output
CYCLE = 14.0       # full loop seconds

evs, t = [], T0
for kind, text, color in LINES:
    if kind == 'cmd':
        evs.append((t, len(text) * CPS, kind, text, color))
        t += len(text) * CPS + 0.25
    else:
        evs.append((t, 0.02, kind, text, color))
        t += GAP_CMD
END = min(t + 0.4, CYCLE - 1.2)
assert END < CYCLE

H = TOP + LH * len(LINES) + 46

def esc(s):
    return html.escape(s, quote=False)

css, body, defs = [], [], []
for i, (t_start, dur, kind, text, color) in enumerate(evs):
    y = TOP + LH * i
    w = len(text) * CH + 2
    steps = len(text) if kind == 'cmd' else 1
    p0 = 100.0 * t_start / CYCLE
    p1 = 100.0 * min(t_start + dur, CYCLE) / CYCLE
    css.append(f'@keyframes r{i}{{0%,{p0:.2f}%{{width:0}}{p1:.2f}%,100%{{width:{w:.0f}px}}}}')
    css.append(f'#c{i} rect{{animation:r{i} {CYCLE}s steps({steps}) infinite;}}')
    if kind == 'cmd':
        u = text.index('$')
        pre, post = text[:u + 1], text[u + 1:]
        spans = f'<tspan fill="#7ee787">{esc(pre)}</tspan><tspan fill="#e6edf3">{esc(post)}</tspan>'
    else:
        spans = f'<tspan fill="{color}">{esc(text)}</tspan>'
    body.append(f'<g clip-path="url(#c{i})"><text x="{PAD_X}" y="{y}" class="t">{spans}</text></g>')
    defs.append(f'<clipPath id="c{i}"><rect x="{PAD_X}" y="{y - FS}" width="0" height="{LH}"/></clipPath>')

# blinking cursor after last output line
cy = TOP + LH * len(LINES)
cp = 100.0 * END / CYCLE
css.append(f'@keyframes cur{{0%,{cp:.2f}%{{opacity:0}}{cp + 0.01:.2f}%,100%{{opacity:1}}}}')
css.append(f'@keyframes blk{{0%,49.9%{{opacity:1}}50%,100%{{opacity:0}}}}')
css.append(f'#cur{{animation:cur {CYCLE}s linear infinite, blk 1.1s steps(1) infinite;}}')
body.append(
    f'<text x="{PAD_X}" y="{cy}" class="t"><tspan fill="#7ee787">ghost@pookie:~$ </tspan></text>'
    f'<rect id="cur" x="{PAD_X + 16 * CH}" y="{cy - FS + 3}" width="{CH}" height="{FS + 4}" fill="#e6edf3"/>'
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
.t{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:{FS}px;}}
{''.join(css)}
</style>
<defs>{''.join(defs)}</defs>
<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>
<rect width="{W}" height="32" rx="10" fill="#161b22"/>
<rect y="16" width="{W}" height="16" fill="#161b22"/>
<circle cx="20" cy="16" r="5.5" fill="#ff5f57"/>
<circle cx="38" cy="16" r="5.5" fill="#febc2e"/>
<circle cx="56" cy="16" r="5.5" fill="#28c840"/>
<text x="{W / 2}" y="20" class="t" font-size="12" fill="#8b949e" text-anchor="middle">ghost@pookie: ~</text>
{''.join(body)}
</svg>
'''

open('terminal.svg', 'w', encoding='utf-8').write(svg)
print('terminal.svg', len(svg), 'bytes | timeline end %.1fs of %.1fs cycle' % (END, CYCLE))
