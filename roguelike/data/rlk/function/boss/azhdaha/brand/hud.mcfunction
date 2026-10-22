# The sub-line part "낙인(<element>) N초" of the branded player (rebuilt with the lines).
data remove storage rlk:mboss az.hud.br
execute unless entity @a[tag=player,scores={azBrT=1..},limit=1] run return 0
execute store result storage rlk:mboss az.hb.n int 1 run scoreboard players get @a[tag=player,scores={azBrT=1..},limit=1] azBrT
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=1}] run data modify storage rlk:mboss az.hb.e set value "불"
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=2}] run data modify storage rlk:mboss az.hb.e set value "물"
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=3}] run data modify storage rlk:mboss az.hb.e set value "번개"
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=4}] run data modify storage rlk:mboss az.hb.e set value "얼음"
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=1}] run data modify storage rlk:mboss az.hb.c set value "#FF8A3D"
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=2}] run data modify storage rlk:mboss az.hb.c set value "#4FB8FF"
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=3}] run data modify storage rlk:mboss az.hb.c set value "#C58BFF"
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=4}] run data modify storage rlk:mboss az.hb.c set value "#9FE8F5"
function rlk:boss/azhdaha/brand/hud_set with storage rlk:mboss az.hb
