# A small meteor lands: the blast and a fire field r 2.8 / 160 t.
function rlk:boss/azhdaha/fx/p/impact/1
function rlk:boss/azhdaha/fx/snd/meteor_small
data modify storage rlk:mboss az.nf set value {fam:1,r:28,len:0,w:0,life:160,dmg:8,sh:0,area:25,rule:0,yaw:-999}
data modify storage rlk:mboss az.nf.el set value 1
function rlk:boss/azhdaha/fld/new
function rlk:boss/azhdaha/p/firefield/amb_on
