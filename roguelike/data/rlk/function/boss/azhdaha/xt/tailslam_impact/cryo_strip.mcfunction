# E+2 (as the body at the tail root, rotated along the line): the strip field.
data modify storage rlk:mboss az.nf set value {fam:3,r:0,len:130,w:35,life:60,dmg:13,sh:1,area:46,rule:0,yaw:-999}
execute store result storage rlk:mboss az.nf.el int 1 run scoreboard players get #azET mb
function rlk:boss/azhdaha/fld/new
