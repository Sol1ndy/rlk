# E+8 (as the body, 5 b along the end line from the tail root, rotated along it): the hail strip.
data modify storage rlk:mboss az.nf set value {fam:2,r:0,len:70,w:35,life:60,dmg:13,sh:1,area:24,rule:0,yaw:-999}
execute store result storage rlk:mboss az.nf.el int 1 run scoreboard players get #azET mb
function rlk:mboss/azhdaha/fld/new
