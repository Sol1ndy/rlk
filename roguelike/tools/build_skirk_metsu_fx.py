"""Author Metsu's separated straight cuts inside its existing forward damage area.

This changes release VFX only. The six damage beats, coefficients, locked heading,
charge animation and Jin burst remain owned by their existing functions.
Run with --datapack <path>; defaults to the datapack containing this tool.
"""
from pathlib import Path
import argparse
import math


# Runtime local coordinates: +Z forward, +Y up. Every endpoint sits within the
# forward damage sphere centered at (0, 0, 3.5), radius 4.5. Each beat has its own
# near/far and left/right locations; no pair shares a center or forms a fixed X.
BASE_CUTS = {
    29: [((-3.10, .45, 2.00), (-1.25, 2.00, 2.65)),
         ((1.00, 1.25, 5.25), (3.00, 1.60, 4.95))],
    31: [((1.55, 2.05, 1.60), (3.20, .50, 2.00)),
         ((-2.15, .60, 5.40), (-1.80, 2.25, 5.95))],
    33: [((-.95, 1.65, 6.20), (1.25, 1.90, 6.30)),
         ((-3.20, 1.90, 3.40), (-2.25, .45, 4.20))],
    35: [((2.10, .60, 3.30), (2.60, 2.45, 4.10)),
         ((-.90, .70, .85), (.95, 1.35, 1.35))],
    37: [((-3.20, 1.30, 4.65), (-.70, 1.85, 4.80)),
         ((1.60, 2.10, 5.60), (1.25, .50, 6.10))],
    41: [((-3.25, .40, 2.60), (-1.90, 2.35, 3.00)),
         ((-.60, 1.00, 1.45), (1.15, 1.70, 1.75)),
         ((1.50, 2.20, 3.80), (3.30, .60, 4.35)),
         ((-1.25, .45, 6.15), (.40, 2.20, 6.40))],
}


def enlarged_cut(a, b):
    """Longer, taller cuts while keeping endpoints inside the existing AoE."""
    center = tuple((x+y)/2 for x,y in zip(a,b))
    endpoints = []
    for endpoint in (a,b):
        enlarged = [center[i] + (endpoint[i]-center[i])*1.62 for i in range(3)]
        enlarged[1] = .20 + enlarged[1]*1.25
        enlarged[1] = max(.16, enlarged[1])
        relative = (enlarged[0], enlarged[1], enlarged[2]-3.5)
        length = math.sqrt(sum(v*v for v in relative))
        if length > 4.35:
            relative = tuple(v*4.35/length for v in relative)
            enlarged = [relative[0],relative[1],relative[2]+3.5]
        endpoints.append(tuple(enlarged))
    return tuple(endpoints)


CUTS = {tick:[enlarged_cut(a,b) for a,b in segments]
        for tick,segments in BASE_CUTS.items()}

WHITE = (.90, .98, 1.00)
CYAN = (.32, .78, 1.00)
VIOLET = (.40, .16, .92)
DARK = (.08, .035, .18)


def number(value):
    return f'{value:.4f}'.rstrip('0').rstrip('.') or '0'


def local(point):
    return ' '.join('^' + number(v) for v in point)


def at(a, b, fraction):
    return tuple(x + (y - x) * fraction for x, y in zip(a, b))


def particle(kind, point, spread='0 0 0', speed=0, count=1):
    return (f'particle minecraft:{kind} {local(point)} {spread} '
            f'{number(speed)} {count} force @a[distance=..64]')


def dust(color, scale):
    values = ','.join(number(c) + 'f' for c in color)
    return f'dust{{color:[{values}],scale:{number(scale)}f}}'


def line(a, b, color, scale, spacing=.14, start=0, end=1):
    length = math.dist(a, b) * (end - start)
    count = max(2, math.ceil(length / spacing) + 1)
    return [particle(dust(color, scale), at(a, b, start + (end-start)*i/(count-1)))
            for i in range(count)]


def slash(segments, final=False):
    result = []
    for index, (a, b) in enumerate(segments):
        # The violet/cyan sheath and narrow white center describe ONE straight
        # cut, rather than two diagonals attached to the same forward point.
        result += line(a, b, VIOLET if index % 2 == 0 else CYAN,
                       1.70 if final else 1.40, .105)
        result += line(a, b, WHITE, .70 if final else .56, .085)
        result.append(particle('end_rod', at(a, b, .88), '.04 .04 .04', 0, 3))
    return result


def afterglow(segments, scale=.40):
    result = []
    for a, b in segments:
        result += line(a, b, CYAN, scale, .23, .15, .85)
    return result


def build(datapack):
    fx = datapack / 'data/rlk/function/char/motion/skirk_fx'
    directory = fx / 'burst_metsu'
    frames = {tick: [] for tick in (*range(28, 45), 46, 48, 50)}

    # Charge gives way to two separate points in the damage field, not a central
    # disc/ray that would make all later cuts look like one crossed path.
    for a, b in CUTS[29]:
        frames[28] += line(a, b, DARK, .43, .30, .38, .62)

    for tick, segments in CUTS.items():
        frames[tick] = slash(segments, final=tick == 41)
        frames[tick + 1] = afterglow(segments, .72 if tick == 41 else .54)

    # The short pause before the last hit gathers light independently at the
    # four final cut locations. The final beat then cuts all four locations.
    for tick, scale in ((39, .32), (40, .58)):
        for a, b in CUTS[41]:
            frames[tick] += line(a, b, VIOLET, scale, .25, .42, .58)

    for tick, scale, fraction in ((43, .34, .65), (44, .28, .70),
                                  (46, .22, .76), (48, .18, .82),
                                  (50, .14, .88)):
        for a, b in CUTS[41]:
            center = at(a, b, fraction)
            center = (center[0], center[1] - (tick-42)*.025, center[2])
            frames[tick].append(particle(dust(CYAN, scale), center))

    directory.mkdir(parents=True, exist_ok=True)
    for tick, commands in frames.items():
        header = ('# Generated by tools/build_skirk_metsu_fx.py. '
                  'Separated straight cuts; locked local heading.\n')
        (directory/f't{tick:03}.mcfunction').write_text(
            header + '\n'.join(commands) + '\n', encoding='utf-8')

    # Charge frames 0..26 are deliberately not regenerated by this tool.
    ticks = sorted(int(p.stem[1:]) for p in directory.glob('t*.mcfunction'))
    dispatcher = [
        '# Skirk Metsu VFX. @s = player; position = actual body; locked clip heading.',
        '# Charge 0..26 is preserved; release uses separated straight cuts within the forward AoE.',
        '# Six damage beats remain 29, 31, 33, 35, 37 and 41.',
        *[f'execute if score @s pmTick matches {t} run function '
          f'rlk:char/motion/skirk_fx/burst_metsu/t{t:03}' for t in ticks],
    ]
    (fx/'burst_metsu.mcfunction').write_text('\n'.join(dispatcher) + '\n', encoding='utf-8')
    print(f'Built Metsu release VFX: {len(CUTS)} beats, '
          f'{sum(map(len, CUTS.values()))} separate straight cuts, {len(frames)} frames.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datapack', type=Path, default=Path(__file__).resolve().parents[1])
    build(parser.parse_args().datapack)
