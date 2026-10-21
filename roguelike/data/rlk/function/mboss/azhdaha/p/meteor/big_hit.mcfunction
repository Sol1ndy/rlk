# The big impact: the dome, the boom, a fire field r 4.5 / 200 t.
function rlk:mboss/azhdaha/fx/p/fire_dome {r:52}
function rlk:mboss/azhdaha/fx/snd/meteor_impact
data modify storage rlk:mboss az.nf set value {fam:1,r:45,len:0,w:0,life:200,dmg:8,sh:0,area:64,rule:0,yaw:-999}
data modify storage rlk:mboss az.nf.el set value 1
function rlk:mboss/azhdaha/fld/new
function rlk:mboss/azhdaha/p/firefield/amb_on
