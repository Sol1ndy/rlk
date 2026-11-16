# @s = a live zone hazard (r 2.8): its dark disc decal again, full size, with the remaining tell.
scoreboard players operation #fgX mb = @s mbHzW
scoreboard players operation #fgX mb -= @s mbHzT
scoreboard players remove #fgX mb 1
execute if score #fgX mb matches ..0 run return 0
execute store result storage rlk:mboss fg.rd.tell int 1 run scoreboard players get #fgX mb
data modify storage rlk:mboss fg.rd merge value {r0:28,r:28,grow:1,hold:0}
execute rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/dark with storage rlk:mboss fg.rd
