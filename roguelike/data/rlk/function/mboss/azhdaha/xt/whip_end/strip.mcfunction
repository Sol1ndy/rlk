# E+15 (as the body at the end-line point, rotated along it): the Electro strip.
data modify storage rlk:mboss az.nf set value {fam:3,r:0,len:120,w:40,life:80,dmg:16,sh:1,area:48,rule:0,yaw:-999}
execute store result storage rlk:mboss az.nf.el int 1 run scoreboard players get #azET mb
function rlk:mboss/azhdaha/fld/new
