"""S5: the effect panels of final_fight.jpg (kit functions in the harness, render_kn_core's card ray caster)."""
import sys
from pathlib import Path
S = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
OUT = S / 'ar/review/rend'
sys.argv = [sys.argv[0], str(S / 'ar/wt_i1/roguelike'), str(S / 'ar/rp_i1'), str(OUT)]
sys.path.insert(0, str(S / 'ar/s1k/render'))
import render_kn_core as R  # noqa: E402
from PIL import ImageDraw  # noqa: E402
G, api, np = R.G, R.api, R.np
W, H = 320, 210
BODY = [((0.0, 0.7, 0.0), (0.3, 0.7, 0.25), (0.14, 0.12, 0.12)), ((0.0, 1.8, 0.0), (0.4, 0.55, 0.27), (0.85, 0.85, 0.82)),
        ((0.0, 2.55, 0.0), (0.21, 0.24, 0.21), (0.9, 0.88, 0.86))]


def standin(at):
    def draw(img, cam, depth):
        O, D = cam.rays()
        for off, rad, col in BODY:
            c = np.array(at) + np.array(off)
            lo = (O - c) / np.array(rad)
            ld = D / np.array(rad)
            A = (ld * ld).sum(-1)
            B = 2 * (lo * ld).sum(-1)
            C = (lo * lo).sum(-1) - 1
            disc = B * B - 4 * A * C
            t = np.full(A.shape, np.inf)
            ok = disc >= 0
            t1 = (-B - np.sqrt(np.where(ok, disc, 0))) / (2 * A)
            good = ok & (t1 > 1e-4)
            t[good] = t1[good]
            m = t < depth
            if m.any():
                img[m] = np.array(col)
                depth[m] = t[m]
    return draw


def label(im, txt):
    ImageDraw.Draw(im).text((4, 4), txt, fill=(255, 255, 255), font=R.font(11))
    return im


P0 = (760.5, R.FY, 8.5)
# 1. B1: the flaming scythe wheel (prop wheel on a projectile display + its fire trail), from the side
s = R.fresh()
s.run('summon minecraft:item_display 760.5 202.2 10.5 {Tags:["rlk_kn_p"],teleport_duration:1}')
d = [e for e in s.ents if e.etype == 'item_display'][0]
d.rot = [0.0, 0.0]
s.run(api.K.prop('wheel'), ex=d)
s.run(G.fx('wheel_trail', len=60), pos=(760.5, R.FY, 10.5), rot=(0.0, 0.0))
for _ in range(5):
    d.pos = list(R.mcsim.Sim.local(s, R.mcsim.Ctx(d, tuple(d.pos), tuple(d.rot)), 0, 0, 0.6))
    s.tick(1)
cam = R.view_cam((763.5, R.FY + 2.4, d.pos[2] + 7.0), (760.5, R.FY + 1.3, d.pos[2] - 0.5), W, H, fov=60)
im1 = label(R.render(cam, R.sim_cards(s), s.gt, bg=(0.42, 0.5, 0.56), dts=R.dots(s), extra=standin(P0)),
            'B1 flaming scythe wheel (3/4 front)')
# 2. F1: the Banquet's flood (t 50, 6 t flash) + the threads falling at hit1
s = R.fresh()
s.run(G.decal('flood', r=260, t=50), pos=P0)
s.tick(44)
s.run(G.fx('threads', r=260), pos=P0)
s.tick(2)
cam = R.view_cam((760.5 + 12, R.FY + 11, 8.5 + 20), (760.5, R.FY + 0.8, 8.5), W, H, fov=70)
im2 = label(R.render(cam, R.sim_cards(s), s.gt, bg=(0.42, 0.5, 0.56), dts=R.dots(s), extra=standin(P0)),
            'F1 Banquet: flood flash + threads')
# 3. Q4: aim line + reticle, then the beam, from the side
s = R.fresh()
chest = (760.5, R.FY + 4.0 + 1.8, 8.5)
s.run(G.fx('reticle'), pos=chest, rot=(0.0, 20.0))
s.tick(20)
s.run(G.fx('beam', len=150), pos=chest, rot=(0.0, 20.0))
s.tick(2)
cam = R.view_cam((760.5 + 11, R.FY + 3.0, 8.5 + 6), (760.5, R.FY + 2.5, 8.5 + 6), W, H, fov=70)
im3 = label(R.render(cam, R.sim_cards(s), s.gt, bg=(0.42, 0.5, 0.56), dts=R.dots(s), extra=standin((760.5, R.FY + 4.0, 8.5))),
            'Q4 reticle + beam (side, 4 b up)')
# 4. Q5B: the vertical X (front)
s = R.fresh()
s.run(G.fx('x_mark'), pos=P0, rot=(0.0, 0.0))
s.tick(66)
cam = R.view_cam((760.5 + 2.0, R.FY + 2.0, 8.5 + 9), (760.5, R.FY + 2.0, 8.5 + 1.0), W, H, fov=60)
im4 = label(R.render(cam, R.sim_cards(s), s.gt, bg=(0.42, 0.5, 0.56), dts=R.dots(s), extra=standin(P0)),
            'Q5B vertical X (front, white-hot)')
for i, im in enumerate((im1, im2, im3, im4)):
    im.save(OUT / f'fx{i + 1}.png')
print('ok')
