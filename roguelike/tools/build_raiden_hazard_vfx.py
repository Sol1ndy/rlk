"""Native display meshes for all twelve Narukami hazard volumes.

Called by build_raiden_hazards.py. One owned display holds a whole warning or
strike, regardless of the number of branches in its mesh. The hit generator
remains the authority for positions, yaw, timing, and the jumpable ring radius.
"""
from pathlib import Path
import json
import math
import sys

SCALE = 32
TEXTURES = {
    "purple": "rlk:raiden/fx/violet_dense",
    "blue": "rlk:raiden/fx/blue",
    "light": "rlk:raiden/fx/cyan",
    "white": "rlk:raiden/fx/white",
    "dark": "rlk:raiden/fx/shadow",
    "violet": "rlk:raiden/fx/violet",
    "lavender": "rlk:raiden/fx/lavender",
    "glow": "rlk:raiden/fx/glow",
    "after": "rlk:raiden/fx/afterglow",
    "fill": "rlk:raiden/fx/floor",
    "void": "rlk:raiden/fx/void",
    "particle": "rlk:raiden/fx/violet_dense",
}
FACES = ("north", "south", "east", "west", "up", "down")


def build(root, out):
    rp = root.parent / "resourcepack"
    if "--resourcepack" in sys.argv:
        rp = Path(sys.argv[sys.argv.index("--resourcepack") + 1])
    from build_raiden_materials import build_materials
    build_materials(rp)
    modeldir = rp / "assets/rlk/models/item/raiden/fx_hazard"
    itemdir = rp / "assets/rlk/items/raiden/fx_hazard"
    modeldir.mkdir(parents=True, exist_ok=True)
    itemdir.mkdir(parents=True, exist_ok=True)

    def write(name, lines):
        path = out / (name + ".mcfunction")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def box(mesh, a, b, color):
        # All native elements stay inside -16..32. Model [8,8,8] is the
        # marker origin; item-display scale32 recovers exact world units.
        mesh.append({"shade": False,
                     "from": [round(8 + min(a[i], b[i]) * 16/SCALE, 5) for i in range(3)],
                     "to": [round(8 + max(a[i], b[i]) * 16/SCALE, 5) for i in range(3)],
                     "faces": {f: {"texture": "#"+color, "uv": [0, 0, 16, 16]} for f in FACES}})

    def stroke(mesh, points, width, color, thickness=None, vertical=False):
        """Connected short cuboids: crisp voxel lightning, no illegal rotations."""
        thickness = width if thickness is None else thickness
        for a, b in zip(points, points[1:]):
            n = max(1, math.ceil(math.dist(a, b)/.62))
            for i in range(n):
                p = tuple(a[k] + (b[k]-a[k])*i/n for k in range(3))
                q = tuple(a[k] + (b[k]-a[k])*(i+1)/n for k in range(3))
                pad = (width/2, width/2, thickness/2) if vertical else (width/2, thickness/2, width/2)
                box(mesh, [min(p[k], q[k])-pad[k] for k in range(3)],
                    [max(p[k], q[k])+pad[k] for k in range(3)], color)

    def lightning(mesh, points, width=.24, residue=False, vertical=False, taper=False):
        # True alpha shells blend with terrain and with the narrower bright
        # center. The white filament is deliberately thin: violet inner edge,
        # lavender halo and dark gaps supply the contrast instead of a solid bar.
        segments = [(points,width)]
        if taper:
            count=max(1,len(points)-1)
            segments=[([a,b],width*(1-.58*i/count)) for i,(a,b) in enumerate(zip(points,points[1:]))]
        for path,w in segments:
            if residue:
                stroke(mesh, path, w*1.1, "after", w*.8, vertical)
                stroke(mesh, path, w*.38, "lavender", w*.6, vertical)
            else:
                stroke(mesh, path, w*1.85, "glow", w*1.35, vertical)
                stroke(mesh, path, w, "purple", w*.78, vertical)
                stroke(mesh, path, w*.17, "white", w*.92, vertical)

    def circle(r, y=.075, start=-180, end=180, step=8):
        n = max(3, math.ceil(abs(end-start)/step))
        return [(r*math.sin(math.radians(start+(end-start)*i/n)), y,
                 r*math.cos(math.radians(start+(end-start)*i/n))) for i in range(n+1)]

    def rect(length, width, y=.075):
        w = width/2
        return [(-w,y,0), (-w,y,length), (w,y,length), (w,y,0), (-w,y,0)]

    def rot(points, angle):
        s, c = math.sin(math.radians(angle)), math.cos(math.radians(angle))
        return [(x*c+z*s, y, z*c-x*s) for x,y,z in points]

    def sector(radius, half):
        return [(0,.075,0)] + circle(radius, .075, -half, half) + [(0,.075,0)]

    def outline(shape):
        if shape in (1,4):
            r,a = (6,60) if shape == 1 else (12,70)
            return [sector(r,a)]
        if shape in (3,6,8,12):
            return [circle({3:3,6:5,8:6,12:12}[shape])]
        if shape == 9:
            return [rot(rect(18,.9), a) for a in (-40,-20,0,20,40)]
        if shape == 11:
            return [circle(1.3),circle(2.7)]
        length,width = {2:(12,2.2),5:(20,3.6),7:(8,8),10:(18,7)}[shape]
        return [rect(length,width)]

    def warning(shape,charge=-1):
        mesh=[]
        # A faint plane makes the area readable while preserving the floor.
        # Its geometry is wholly inside the analytic hit boundary.
        if shape in (1,4):
            radius, half = (6,60) if shape==1 else (12,70)
            for i in range(1,36):
                z=radius*i/36
                dz=radius/36
                halfwidth=min(z*math.tan(math.radians(half)), math.sqrt(max(0,radius*radius-(z+dz)**2)))
                if halfwidth>.04:
                    box(mesh,(-halfwidth,.025,z),(halfwidth,.029,z+dz),"fill")
        elif shape in (2,5,7,10):
            length,width={2:(12,2.2),5:(20,3.6),7:(8,8),10:(18,7)}[shape]
            box(mesh,(-width/2,.025,0),(width/2,.029,length),"fill")
        elif shape in (3,6,8,12):
            radius={3:3,6:5,8:6,12:12}[shape]
            for i in range(-24,24):
                z0,z1=radius*i/24,radius*(i+1)/24
                halfwidth=math.sqrt(max(0,radius*radius-max(z0*z0,z1*z1)))
                if halfwidth>.04:
                    box(mesh,(-halfwidth,.025,z0),(halfwidth,.029,z1),"fill")
        for path in outline(shape):
            # Low dark edging keeps the tell legible on light gray arena floors.
            stroke(mesh,[(x,y-.023,z) for x,y,z in path],.27,"void",.020)
            stroke(mesh,[(x,y-.012,z) for x,y,z in path],.50,"glow",.016)
            stroke(mesh,path,.14,"purple",.029)
            # Smaller luminous line lies visibly above the violet border.
            stroke(mesh,[(x,y+.023,z) for x,y,z in path],.042,"light",.017)
            if charge>=0:
                stroke(mesh,[(x,y+.045,z) for x,y,z in path],.105,"white",.025)
                # Final four ticks energize the same boundary with short
                # upward sparks. They never resemble the full attack path.
                stride=max(1,(len(path)-1)//7)
                for i in range(charge,len(path)-1,stride):
                    x,y,z=path[i]
                    cx,cz=0,0
                    if shape in (1,4): cz=2 if shape==1 else 4
                    if shape in (2,5,7,10): cz={2:6,5:10,7:4,10:9}[shape]
                    dx,dz=cx-x,cz-z
                    norm=max(.001,math.hypot(dx,dz))
                    dx,dz=dx/norm,dz/norm
                    lift=.28+.14*charge
                    lightning(mesh,[(x,.12,z),(x+dx*.12,.25,z+dz*.12),
                                    (x+dx*.36,lift,z+dz*.36)],.11,vertical=True,taper=True)
        # Direction chevrons and sparse hatching make filled attack areas
        # understandable without opaque carpets hiding player feet.
        if shape in (1,4):
            r,a = (6,60) if shape == 1 else (12,70)
            for ang in (-a*.55,0,a*.55):
                stroke(mesh,rot([(0,.06,1),(0,.06,r-.25)],ang),.055,"purple",.02)
            stroke(mesh,circle(r*.57,.06,-a,a),.055,"violet",.02)
        elif shape in (2,5,7,10):
            length,width = {2:(12,2.2),5:(20,3.6),7:(8,8),10:(18,7)}[shape]
            for z in range(2,length,3):
                stroke(mesh,[(-min(.6,width*.3),.08,z-.4),(0,.08,z),
                             (min(.6,width*.3),.08,z-.4)],.09,"light",.03)
        elif shape == 9:
            for a in (-40,-20,0,20,40):
                for z in (5,11,16):
                    stroke(mesh,rot([(-.25,.08,z-.4),(0,.08,z),(.25,.08,z-.4)],a),.07,"light",.03)
        elif shape in (3,6,8,12):
            r={3:3,6:5,8:6,12:12}[shape]
            stroke(mesh,circle(r*.46,.06),.065,"violet",.02)
            for a in (0,90,180,270):
                stroke(mesh,rot([(0,.07,r*.67),(0,.07,r-.2)],a),.10,"light",.025)
            stroke(mesh,[(-.5,.08,0),(.5,.08,0)],.10,"light",.025)
            stroke(mesh,[(0,.08,-.5),(0,.08,.5)],.10,"light",.025)
        return mesh

    def forward_bolt(length, spread, y=1.2, offset=0,variant=0):
        return [(offset+(0 if i in (0,10) else spread*((-1)**(i+variant))),
                 y+(.18 if (i+variant)%3==1 else -.12 if (i+variant)%3==2 else 0),
                 length*i/10) for i in range(11)]

    def branch_column(mesh,x,z,height,residue=False,variant=0,width=.34):
        flip=-1 if variant%2 else 1
        path=[(x,.1,z),(x-.3*flip,height*.16,z+.12),
              (x+.28*flip,height*.34,z-.12),(x-.18*flip,height*.56,z+.08),
              (x+.45*flip,height*.78,z-.15),(x-.22*flip,height,z)]
        lightning(mesh,path,width,residue,True,True)
        if not residue:
            lightning(mesh,[(x+.28*flip,height*.34,z-.12),(x+1.0*flip,height*.49,z+.25),
                            (x+.65*flip,height*.63,z+.4)],width*.5,False,True,True)
            lightning(mesh,[(x-.18*flip,height*.56,z+.08),(x-.85*flip,height*.67,z-.35),
                            (x-1.1*flip,height*.83,z-.2)],width*.32,False,True,True)

    def blade_crescent(mesh,radius,angle,residue,variant):
        # A shallow folded ribbon makes the sword's cutting plane readable,
        # with the light edge exposed above its violet body.
        n=32
        edge=[]
        for i in range(n+1):
            u=i/n
            a=math.radians(-angle+2*angle*u)
            r=radius*(.92+.018*math.sin(i*2.3+variant))
            y=.70+1.15*math.sin(math.pi*u)+.045*variant
            edge.append((r*math.sin(a),y,r*math.cos(a)))
        for i,(a,b) in enumerate(zip(edge,edge[1:])):
            u=(i+.5)/n
            width=.10+.50*math.sin(math.pi*u)
            center=math.radians(-angle+2*angle*u)
            ox,oz=-math.sin(center)*width,-math.cos(center)*width
            box(mesh,(min(a[0],b[0],a[0]+ox,b[0]+ox),min(a[1],b[1])-.095,
                      min(a[2],b[2],a[2]+oz,b[2]+oz)),
                     (max(a[0],b[0],a[0]+ox,b[0]+ox),max(a[1],b[1])+.015,
                      max(a[2],b[2],a[2]+oz,b[2]+oz)),"after" if residue else "violet")
        if not residue:
            lightning(mesh,[(x,y+.075,z) for x,y,z in edge],.13,False)

    def rising_cleave(mesh,length,residue,variant):
        # The full blade-shaped rupture is present on impact. Its successive
        # frames alter folds/forks only; no late traveling hit is implied.
        spine=[]
        n=28
        for i in range(n+1):
            u=i/n
            x=.24*math.sin(i*1.8+variant)
            y=.65+3.2*math.sin(math.pi*u)**.8
            spine.append((x,y,.15+(length-.3)*u))
        for i,(a,b) in enumerate(zip(spine,spine[1:])):
            upper=min(a[1],b[1])
            box(mesh,(min(a[0],b[0])-.12,.20,a[2]),
                     (max(a[0],b[0])+.12,upper,b[2]),"after" if residue else "violet")
            if not residue:
                # These narrow blue faces protrude on either side of the
                # blade sheet, enriching color without enclosing the core.
                box(mesh,(min(a[0],b[0])-.135,max(.22,upper-.48),a[2]),
                         (max(a[0],b[0])+.135,upper-.10,b[2]),"blue")
        if not residue:
            lightning(mesh,[(x,y+.06,z) for x,y,z in spine],.23,False)
            for i in (5,11,18,24):
                x,y,z=spine[i]
                sign=-1 if (i+variant)%2 else 1
                lightning(mesh,[(x,y*.65,z),(sign*.85,y*.82,z+.30),
                                (sign*1.45,y*.55,z+.65)],.18,False,True,True)

    def strike(shape,residue=False,variant=0):
        mesh=[]
        if shape in (1,4):
            radius,angle=(6,60) if shape==1 else (12,70)
            for fraction,y in ((.30,.55),(.62,1.05),(.94,1.5)):
                path=circle(radius*fraction,y,-angle,angle,7)
                jag=[(x*(1+(.027 if (i+variant)%2 else -.027)),h+(.18 if (i+variant)%2 else -.18),
                      z*(1+(.027 if (i+variant)%2 else -.027))) for i,(x,h,z) in enumerate(path)]
                lightning(mesh,jag,.24 if shape==1 else .36,residue)
            for a in (-angle*.65,0,angle*.65):
                lightning(mesh,rot(forward_bolt(radius-.25,.20,.8,variant=variant),a),.14,residue,taper=True)
            blade_crescent(mesh,radius,angle,residue,variant)
        elif shape in (3,6,8,12):
            radius={3:3,6:5,8:6,12:12}[shape]
            branch_column(mesh,0,0,7 if shape==3 else 9,residue,variant,.45)
            count=4 if radius<6 else 6
            for i in range(count):
                angle=360*i/count
                s,c=math.sin(math.radians(angle)),math.cos(math.radians(angle))
                if radius>=5:
                    branch_column(mesh,s*radius*.63,c*radius*.63,3.8,residue,(variant+i)%3,.26)
                lightning(mesh,rot(forward_bolt(radius-.25,.30,.35,variant=variant),angle),.20,residue,taper=True)
            lightning(mesh,circle(radius*.94,.28),.21,residue)
        elif shape in (2,5,9,10):
            length={2:12,5:20,9:18,10:18}[shape]
            angles=(-40,-20,0,20,40) if shape==9 else (0,)
            offsets=(-2.8,0,2.8) if shape==10 else (0,)
            for a in angles:
                for offset in offsets:
                    lightning(mesh,rot(forward_bolt(length,.24 if shape==9 else .38,1.2,offset,variant),a),
                              .22 if shape==9 else .32,residue,taper=True)
                    if shape != 9:
                        # Charged spines visibly fill the blade/energy corridor.
                        for z in range(2,length,4):
                            reach=.70 if shape==2 else 1.5 if shape==5 else .55
                            lightning(mesh,[(offset-reach,.25,z-.6),(offset-.2,1.2,z),
                                            (offset+reach,2.4 if shape==5 else 1.8,z+.6)],.19,residue,True,True)
            if shape==5:
                rising_cleave(mesh,length,residue,variant)
            if shape==10:
                for z in (3,9,15):
                    lightning(mesh,[(-3.35,.35,z),(-2.3,1.6,z+.3),(-.8,2.0,z-.3),
                                    (.8,1.0,z+.3),(2.3,1.6,z-.3),(3.35,.35,z)],.23,residue)
        elif shape==7:
            # Two inward claw/lightning walls meet in a bright central rupture.
            for z in (1.0,3.5,6.0,7.6):
                lightning(mesh,[(-3.8,.4,z),(-2.8,2.5,z+.2),(-1.5,1.65,z-.2),
                                (0,1,z), (1.5,1.65,z+.2),(2.8,2.5,z-.2),(3.8,.4,z)],.32,residue)
            branch_column(mesh,0,4,6,residue,variant,.40)
        return mesh

    def ring(frame):
        radius=2+16*frame/31
        mesh=[]
        # Every active ring depicts the exact damaging +/-0.7 band. Its
        # height stays below0.75 so jumping visibly clears the lightning.
        for r in (radius-.7,radius+.7):
            lightning(mesh,circle(r,.13,step=7),.10)
        for r in (radius-.46,radius+.46):
            stroke(mesh,circle(r,.12,step=7),.30,"glow",.06)
        path=circle(radius,.38,step=7)
        jag=[(x*(1+(.16/radius if i%2 else -.16/radius)),
              .30 if i%2 else .52,z*(1+(.16/radius if i%2 else -.16/radius)))
             for i,(x,y,z) in enumerate(path)]
        lightning(mesh,jag,.23)
        return mesh

    def save(name,mesh,fade=False):
        textures=dict(TEXTURES)
        if fade:
            textures.update(after=TEXTURES["glow"],lavender=TEXTURES["glow"])
        model={"ambientocclusion":False,"gui_light":"front","textures":textures,"elements":mesh}
        (modeldir/(name+".json")).write_text(json.dumps(model,separators=(",",":"))+"\n",encoding="utf-8")
        (itemdir/(name+".json")).write_text(json.dumps({"model":{"type":"minecraft:model", "model":"rlk:item/raiden/fx_hazard/"+name}},separators=(",",":"))+"\n",encoding="utf-8")

    for shape in range(1,13):
        save(f"warning_{shape}",warning(shape))
        for phase in (0,1):
            save(f"charge_{shape}_{phase}",warning(shape,phase))
        if shape !=11:
            save(f"strike_{shape}",strike(shape))
            save(f"strike_{shape}_1",strike(shape,False,1))
            save(f"strike_{shape}_2",strike(shape,False,2))
            save(f"after_{shape}",strike(shape,True))
            save(f"after_{shape}_fade",strike(shape,True),True)
    for frame in range(32):
        save(f"ring_{frame:02}",ring(frame))

    owned='@e[type=minecraft:item_display,tag=rlk_rd_hvfx]'
    new='@e[tag=rlk_rd_vnew,limit=1]'
    modelset=lambda name: 'data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/'+name+'"'
    write("vfx_init",[
        '# One display per fixed hazard origin; all geometry is in its local coordinates.',
        '# Native ItemDisplayRenderer applies Y=180deg after display transformations.',
        '# Right-rotate 180deg to cancel that item-only flip: mesh +Z now equals ^ ^ ^forward.',
        'scoreboard players add #rdHazardSerial rd 1',
        'scoreboard players operation @s rdHId = #rdHazardSerial rd',
        'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_hvfx","rlk_rd_vnew","rlk_raiden_aux","rlk_room"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:0,teleport_duration:0,view_range:3f,width:48f,height:22f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[32f,32f,32f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/warning_1"}}}',
        f'data modify entity {new} Rotation set from entity @s Rotation',
        f'scoreboard players operation {new} rdVId = @s rdHId',
        f'scoreboard players operation {new} rdShape = @s rdShape',
        f'scoreboard players set {new} rdWind 0',
        f'scoreboard players set {new} rdHAge 0',
        f'execute as {new} run function rlk:boss/raiden/hazard/vfx_warning',
        'tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew',
    ])
    write("vfx_warning",[f'execute if score @s rdShape matches {s} run {modelset("warning_"+str(s))}' for s in range(1,13)])
    write("charge",[
        '# Four ticks before impact: charged borders, no full-path strike yet.',
        'scoreboard players operation #rdVfxOwner rd = @s rdHId',
        'scoreboard players set #rdChargeFrame rd 0',
        'execute if score #rdUntil rd matches 1..2 run scoreboard players set #rdChargeFrame rd 1',
        f'execute as {owned} if score @s rdVId = #rdVfxOwner rd run function rlk:boss/raiden/hazard/vfx_charge',
    ])
    write("vfx_charge",['scoreboard players set @s rdWind 2']+[
        f'execute if score @s rdShape matches {s} if score #rdChargeFrame rd matches {p} run {modelset(f"charge_{s}_{p}")}'
        for s in range(1,13) for p in (0,1)
    ])
    write("warning",['# Warning display persists; no repeated particle burst or entity allocation.'])
    for shape in range(1,13):
        write(f"warning/s{shape}",['# Mesh: rlk:raiden/fx_hazard/warning_'+str(shape)])
    write("strike",[
        'scoreboard players operation #rdVfxOwner rd = @s rdHId',
        f'execute as {owned} if score @s rdVId = #rdVfxOwner rd run function rlk:boss/raiden/hazard/vfx_strike',
        'playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.50 1.25 0.2',
        'execute if score @s rdShape matches 4..8 run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.60 1.35 0.25',
        'execute if score @s rdShape matches 12 run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.55 1.5 0.25',
        'function rlk:boss/raiden/hazard/hit',
    ])
    write("vfx_strike",[
        '# Whole path flashes on the exact damage tick; this is instantaneous lightning.',
        'scoreboard players set @s rdWind 1',
        'scoreboard players set @s rdHAge -1',
    ]+[f'execute if score @s rdShape matches {s} run {modelset("strike_"+str(s))}' for s in range(1,13) if s!=11])
    for phase in (1,2):
        write(f"vfx_flash_{phase}",[
            '# The whole area remains lit; only branch topology changes, not hit travel.',
        ]+[f'execute if score @s rdShape matches {s} run {modelset(f"strike_{s}_{phase}")}' for s in range(1,13) if s!=11])
    write("vfx_after",[f'execute if score @s rdShape matches {s} run {modelset("after_"+str(s))}' for s in range(1,13) if s!=11])
    write("vfx_fade",[f'execute if score @s rdShape matches {s} run {modelset("after_"+str(s)+"_fade")}' for s in range(1,13) if s!=11])
    for shape in range(1,13):
        if shape!=11:
            write(f"strike/s{shape}",['# Strike mesh is selected by vfx_strike on the owning display.'])
    for frame in range(32):
        write(f"ring/f{frame:02}",[
            f'# Exact ring radius {2+16*frame/31:.6f}; visible band half-width0.7.',
            'scoreboard players operation #rdVfxOwner rd = @s rdHId',
            f'execute as {owned} if score @s rdVId = #rdVfxOwner rd run {modelset("ring_"+f"{frame:02}")}',
        ])
    write("ring_tick",[
        'scoreboard players operation #rdElapsed rd = @s rdHAge',
        'scoreboard players operation #rdElapsed rd -= @s rdWind',
        'execute if score #rdElapsed rd matches 32.. run return run function rlk:boss/raiden/hazard/expire',
        'execute unless score #rdElapsed rd matches 0..31 run return 0',
        '# Every damage radius receives its matching model in the same tick.',
        'function rlk:boss/raiden/hazard/ring_draw',
        'execute if score #rdElapsed rd matches 0 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.2',
        'execute unless score @s rdHHit matches 1 run function rlk:boss/raiden/hazard/hit',
    ])
    write("vfx_world",[
        '# Call after hazard updates and from pause: removes canceled/orphan effects immediately.',
        f'execute as {owned} run function rlk:boss/raiden/hazard/vfx_tick',
    ])
    write("expire",[
        '# Cancel the display and its parent together; the ring ends at frame32.',
        'scoreboard players operation #rdVfxOwner rd = @s rdHId',
        f'execute as {owned} if score @s rdVId = #rdVfxOwner rd run kill @s',
        'kill @s',
    ])
    write("vfx_tick",[
        'scoreboard players operation #rdVfxOwner rd = @s rdVId',
        'scoreboard players set #rdVfxExists rd 0',
        'execute as @e[tag=rlk_rd_hazard] if score @s rdHId = #rdVfxOwner rd run scoreboard players set #rdVfxExists rd 1',
        'execute if score #rdVfxExists rd matches 0 run return run kill @s',
        'execute unless score @s rdWind matches 1 run return 0',
        'scoreboard players add @s rdHAge 1',
        'execute if score @s rdHAge matches 1 run function rlk:boss/raiden/hazard/vfx_flash_1',
        'execute if score @s rdHAge matches 2 run function rlk:boss/raiden/hazard/vfx_flash_2',
        'execute if score @s rdHAge matches 3 run function rlk:boss/raiden/hazard/vfx_after',
        'execute if score @s rdHAge matches 6 run function rlk:boss/raiden/hazard/vfx_fade',
        'execute if score @s rdHAge matches 9.. run kill @s',
    ])
    # The base generator owns the damage math and lifecycle. Attach creation
    # only after forward-axis caching, preserving its original command order.
    initpath=out/"init.mcfunction"
    original=initpath.read_text(encoding="utf-8")
    original=original.replace('function rlk:boss/raiden/hazard/warning\n',
                              'function rlk:boss/raiden/hazard/vfx_init\n')
    initpath.write_text(original,encoding="utf-8")
    tickpath=out/"tick_at.mcfunction"
    original=tickpath.read_text(encoding="utf-8")
    original=original.replace('run return run kill @s',
                              'run return run function rlk:boss/raiden/hazard/expire')
    original=original.replace('scoreboard players operation #rdMod rd = @s rdHAge',
                              'scoreboard players operation #rdUntil rd = @s rdWind\n'
                              'scoreboard players operation #rdUntil rd -= @s rdHAge\n'
                              'execute if score #rdUntil rd matches 1..4 run function rlk:boss/raiden/hazard/charge\n'
                              'scoreboard players operation #rdMod rd = @s rdHAge')
    tickpath.write_text(original,encoding="utf-8")
    print("Built 123 native display meshes: 12 layered-alpha telegraphs, 24 charge frames, 33 strike frames, 22 fading afterglows, 32 exact ring frames.")
