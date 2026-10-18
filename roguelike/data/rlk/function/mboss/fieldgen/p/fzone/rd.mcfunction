# @s = a live disc hazard (r 2.8): its kit decal with the remaining tell.
scoreboard players operation #fgX mb = @s mbHzW
scoreboard players operation #fgX mb -= @s mbHzT
scoreboard players remove #fgX mb 1
execute if score #fgX mb matches ..0 run return 0
execute store result storage rlk:mboss fg.rd.tell int 1 run scoreboard players get #fgX mb
data modify storage rlk:mboss fg.rd merge value {r:28,el:9,hold:3}
execute rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/disc with storage rlk:mboss fg.rd
