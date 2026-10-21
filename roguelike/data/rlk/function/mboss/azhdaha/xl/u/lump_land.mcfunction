# Positioned at a lump target on landing: the fireball and its fire field (plan 4.6).
function rlk:mboss/azhdaha/fx/p/impact/1
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.5 1.3 0.17
playsound minecraft:block.lava.pop hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
data modify storage rlk:mboss az.nf set value {fam:1,r:40,len:0,w:0,life:160,dmg:8,sh:0,area:50,rule:0,yaw:-999}
data modify storage rlk:mboss az.nf.el set value 1
function rlk:mboss/azhdaha/fld/new
function rlk:mboss/azhdaha/p/firefield/amb_on
