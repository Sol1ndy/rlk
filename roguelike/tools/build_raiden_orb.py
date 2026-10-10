"""Floating remembrance orb and four-quarter hit gauge, owned by rdOvId."""
from pathlib import Path
import argparse
import json
import math

DP=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--resourcepack',required=True)
RP=Path(parser.parse_args().resourcepack)
OUT=DP/'data/rlk/function/boss/raiden/orb'
SCALE=4
T={n:'rlk:raiden/fx/'+n for n in ['void','violet','lavender','white','cyan','shadow','violet_dense','glow','afterglow','pearl']}

def write(name,lines):
 p=OUT/(name+'.mcfunction');p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def box(c,s,color):
 return {'shade':False,'from':[round(8+(c[i]-s[i]/2)*16/SCALE,5) for i in range(3)],
         'to':[round(8+(c[i]+s[i]/2)*16/SCALE,5) for i in range(3)],
         'faces':{f:{'texture':'#'+color,'uv':[0,0,16,16]} for f in ['north','south','east','west','up','down']}}
def line(points,w,color):
 out=[]
 for a,b in zip(points,points[1:]):
  n=max(1,math.ceil(math.dist(a,b)/.08))
  for j in range(n):
   p=[a[i]+(b[i]-a[i])*j/n for i in range(3)];q=[a[i]+(b[i]-a[i])*(j+1)/n for i in range(3)]
   out.append(box([(p[i]+q[i])/2 for i in range(3)],[abs(p[i]-q[i])+w for i in range(3)],color))
 return out
def circle(r,y=0,start=0,end=360,plane='xz'):
 count=max(2,math.ceil(abs(end-start)/9))
 return [(r*math.cos(math.radians(start+(end-start)*i/count)),y,r*math.sin(math.radians(start+(end-start)*i/count))) if plane=='xz'
         else (r*math.cos(math.radians(start+(end-start)*i/count)),r*math.sin(math.radians(start+(end-start)*i/count)),y) for i in range(count+1)]
def shell(radius):
 # Two thin side patches per (height, depth) cell, making a continuous voxel
 # sphere. Alpha51 gives a soft violet globe with its central pearl visible.
 out=[]; step=radius/6
 for iy in range(-6,6):
  y=(iy+.5)*step; rr=math.sqrt(max(0,radius*radius-y*y))
  for iz in range(-6,6):
   z=(iz+.5)*rr/6; x=math.sqrt(max(0,rr*rr-z*z))
   for side in [-1,1]:out.append(box((side*x,y,z),(.018,step+.012,rr/6+.012),'lavender'))
 return out
def model(name,mesh):
 root=RP/'assets/rlk'
 for sub,data in [('models/item',{'ambientocclusion':False,'textures':{**T,'particle':T['violet']},'elements':mesh}),
                  ('items',{'model':{'type':'minecraft:model','model':'rlk:item/raiden/fx_orb/'+name}})]:
  p=root/sub/'raiden/fx_orb'/(name+'.json');p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')

for frame in range(4):
 mesh=shell(.66)
 # Pearl, six suspended petals and thin orbital wisps echo the reference.
 mesh += [box((0,0,0),(.30,.38,.30),'violet_dense'),box((0,.04,0),(.20,.27,.20),'pearl')]
 for i in range(6):
  a=math.radians(i*60+frame*12); x,z=math.cos(a),math.sin(a)
  mesh+=line([(x*.16,-.18,z*.16),(x*.32,-.05,z*.32),(x*.29,.20,z*.29),(x*.12,.32,z*.12)],.09,'violet')
  mesh+=line([(x*.16,-.18,z*.16),(x*.29,.10,z*.29),(x*.12,.32,z*.12)],.022,'pearl')
 for i in range(3):
  mesh+=line(circle(.50+.035*i,(i-1)*.17,frame*18+i*120,frame*18+i*120+75),.025,'pearl')
 # Three geometric comma/rune motifs sit just inside the translucent globe.
 for i in range(3):
  a=math.radians(i*120+frame*8); x,z=.57*math.cos(a),.57*math.sin(a)
  mesh+=line([(x*.88,-.16,z*.88),(x,.04,z),(x*.94,.18,z*.94),(x*.76,.16,z*.76)],.045,'pearl')
 model('orb_'+str(frame),mesh)

for hp in range(5):
 mesh=[]
 for quadrant in range(4):
  start=quadrant*90+9; end=(quadrant+1)*90-9
  mesh+=line(circle(.37,0,start,end,'xy'),.075,'shadow')
  mesh+=line(circle(.37,-.026,start,end,'xy'),.042,'cyan' if quadrant<hp else 'afterglow')
  if quadrant<hp:mesh+=line(circle(.37,-.054,start,end,'xy'),.012,'white')
 # Central dot provides a clean target without numbers or pattern text.
 mesh.append(box((0,0,0),(.07,.07,.035),'pearl'))
 model('gauge_'+str(hp),mesh)

def summon(modelname,tag,y,billboard):
 return 'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_orb","rlk_rd_orb_new","'+tag+'"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_orb/'+modelname+'"}},item_display:"none",billboard:"'+billboard+'",brightness:{block:15,sky:15},width:3f,height:4f,shadow_radius:0f,interpolation_duration:3,start_interpolation:0,transformation:{translation:[0f,'+str(y)+'f,0f],scale:[4f,4f,4f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}'
write('create',[
 '# As the newly initialized kind3 flower, after object_vfx/create assigned rdOvId.',
 'execute unless score @s rdObjKind matches 3 run return 0',
 'scoreboard players operation #rdOrbObject rd = @s rdObjId',
 'execute as @e[tag=rlk_rd_objvisual] if score @s rdObjId = #rdOrbObject rd run kill @s',
 summon('orb_0','rlk_rd_orb_body',1.45,'fixed'),
 'scoreboard players operation @e[tag=rlk_rd_orb_new,limit=1] rdOvId = @s rdOvId',
 'tag @e[tag=rlk_rd_orb_new] remove rlk_rd_orb_new',
 summon('gauge_4','rlk_rd_orb_gauge',2.63,'center'),
 'scoreboard players operation @e[tag=rlk_rd_orb_new,limit=1] rdOvId = @s rdOvId',
 'scoreboard players set @e[tag=rlk_rd_orb_new,limit=1] rdObjHP -1',
 'tag @e[tag=rlk_rd_orb_new] remove rlk_rd_orb_new',
 'function rlk:boss/raiden/orb/tick',
])
tick=[
 '# As flower. HP is the existing one-Electro/four-other attack counter.',
 'scoreboard players operation #rdOrbOwner rd = @s rdOvId',
 'scoreboard players operation #rdOrbHP rd = @s rdObjHP',
 'scoreboard players operation #rdOrbFrame rd = @s rdOAge',
 'scoreboard players set #rdOrbPeriod rd 32',
 'scoreboard players operation #rdOrbFrame rd %= #rdOrbPeriod rd',
 'execute as @e[tag=rlk_rd_orb_gauge] if score @s rdOvId = #rdOrbOwner rd unless score @s rdObjHP = #rdOrbHP rd run function rlk:boss/raiden/orb/gauge',
]
for i in range(8):
 y=1.45+.065*math.sin(i*math.pi/4)
 tick.append(f'execute if score #rdOrbFrame rd matches {i*4} as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data merge entity @s {{start_interpolation:0,interpolation_duration:4,transformation:{{translation:[0f,{y:.4f}f,0f]}}}}')
 if i%2==0:tick.append(f'execute if score #rdOrbFrame rd matches {i*4} as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/orb_{i//2}"')
write('tick',tick)
write('gauge',[
 'scoreboard players operation @s rdObjHP = #rdOrbHP rd',
 *[f'execute if score @s rdObjHP matches {hp} run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/gauge_{hp}"' for hp in range(5)],
])
write('clear',['kill @e[tag=rlk_rd_orb]'])
write('remove',[
 'scoreboard players operation #rdOrbOwner rd = @s rdOvId',
 'execute as @e[tag=rlk_rd_orb] if score @s rdOvId = #rdOrbOwner rd run kill @s',
])
write('world',[
 '# Orphan cleanup for interruption, reload or failed flower: no stale gauge.',
 'execute unless entity @e[tag=rlk_rd_object,scores={rdObjKind=3}] run kill @e[tag=rlk_rd_orb]',
])
print('Built floating remembrance orb: 4 pearl/globe frames, 5 quarter-ring gauge models; owned by rdOvId.')
