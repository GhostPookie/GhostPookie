# Generates terminal.svg: animated Kali-style fake-terminal for the README.
# Pure SVG + CSS, runs inside GitHub's <img> renderer.
import html

FS = 15
LH = 24
CH = 9.0
PAD_X, TOP = 20, 52
W = 760

PROMPT = '┌──(ghost㉿pookie)-[~]'
PS1 = '└─$ '

# each command: prompt line (instant) + typed command + instant outputs
CMDS = [
    ('whoami', ['GhostPookie']),
    ('cat skills.txt', ['python  numpy  scipy  latex  git  linux  bash']),
    ('nmap -sS --top-ports 3 ghost.pookie',
     ['PORT     STATE  SERVICE', '22/tcp   open   ssh',
      '443/tcp  open   https', '1337/tcp open   curiosity']),
    ('uptime', ['1337 days up · load: ideas · 0 crashes']),
]

GRN, GRN_DIM, BLU, WHT, OUT = '#00ff41', '#00b32d', '#00a2ff', '#e6edf3', '#7aff9e'

T0, CPS, GAP = 0.6, 0.04, 0.5
CYCLE = 16.0

evs, t = [], T0
for cmd, outs in CMDS:
    evs.append((t, 0.02, 'prompt', PROMPT, None)); t += 0.08
    evs.append((t, len(cmd) * CPS, 'cmd', cmd, None)); t += len(cmd) * CPS + 0.2
    for o in outs:
        evs.append((t, 0.02, 'out', o, OUT)); t += 0.16
    t += GAP
END = min(t + 0.3, CYCLE - 1.5)

H = TOP + LH * len(evs) + LH + 16

def esc(s):
    return html.escape(s, quote=False)

css, body, defs = [], [], []
for i, (ts, dur, kind, text, color) in enumerate(evs):
    y = TOP + LH * i
    if kind == 'prompt':
        spans = (f'<tspan fill="{GRN}">┌──(ghost</tspan><tspan fill="{WHT}">㉿</tspan>'
                 f'<tspan fill="{GRN}">pookie)</tspan><tspan fill="{BLU}">-[~]</tspan>')
    elif kind == 'cmd':
        spans = f'<tspan fill="{GRN_DIM}">{esc(PS1)}</tspan><tspan fill="{WHT}">{esc(text)}</tspan>'
    else:
        spans = f'<tspan fill="{color}">{esc(text)}</tspan>'
    full_w = len(text) * CH + (len(PS1) * CH if kind == 'cmd' else 0) + 4
    w = full_w if kind != 'cmd' else full_w
    steps = len(text) if kind == 'cmd' else 1
    p0 = 100.0 * ts / CYCLE
    p1 = 100.0 * min(ts + dur, CYCLE) / CYCLE
    css.append(f'@keyframes r{i}{{0%,{p0:.2f}%{{width:0}}{p1:.2f}%,100%{{width:{w:.0f}px}}}}')
    css.append(f'#c{i} rect{{animation:r{i} {CYCLE}s steps({steps}) infinite;}}')
    body.append(f'<g clip-path="url(#c{i})"><text x="{PAD_X}" y="{y}" class="t">{spans}</text></g>')
    defs.append(f'<clipPath id="c{i}"><rect x="{PAD_X}" y="{y - FS}" width="0" height="{LH}"/></clipPath>')

cy = TOP + LH * len(evs)
cp = 100.0 * END / CYCLE
css.append(f'@keyframes cur{{0%,{cp:.2f}%{{opacity:0}}{cp + 0.01:.2f}%,100%{{opacity:1}}}}')
css.append(f'@keyframes blk{{0%,49.9%{{opacity:1}}50%,100%{{opacity:0}}}}')
css.append(f'#cur{{animation:cur {CYCLE}s linear infinite, blk 1.0s steps(1) infinite;}}')
body.append(
    f'<text x="{PAD_X}" y="{cy}" class="t"><tspan fill="{GRN_DIM}">{esc(PS1)}</tspan></text>'
    f'<rect id="cur" x="{PAD_X + len(PS1) * CH}" y="{cy - FS + 3}" width="{CH}" height="{FS + 4}" fill="{GRN}"/>'
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
.t{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:{FS}px;}}
{''.join(css)}
</style>
<defs>{''.join(defs)}</defs>
<rect width="{W}" height="{H}" rx="8" fill="#000000" stroke="{GRN}" stroke-opacity="0.35"/>
<rect width="{W}" height="30" rx="8" fill="#0a0a0a"/>
<rect y="15" width="{W}" height="15" fill="#0a0a0a"/>
<circle cx="19" cy="15" r="5" fill="#ff5f57"/>
<circle cx="36" cy="15" r="5" fill="#febc2e"/>
<circle cx="53" cy="15" r="5" fill="#28c840"/>
<text x="{W / 2}" y="19" class="t" font-size="12" fill="{GRN_DIM}" text-anchor="middle">root@kali: /home/ghost</text>
{''.join(body)}
</svg>
'''

open('terminal.svg', 'w', encoding='utf-8').write(svg)
print('terminal.svg', len(svg), 'bytes | end %.1fs / %.1fs cycle | %d lines' % (END, CYCLE, len(evs)))
