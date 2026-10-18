# @s = a live throw line (dmg 0): its kit line with the remaining tell.
scoreboard players operation #fgX mb = @s mbHzW
scoreboard players operation #fgX mb -= @s mbHzT
scoreboard players remove #fgX mb 1
execute if score #fgX mb matches ..0 run return 0
execute store result storage rlk:mboss fg.rd.tell int 1 run scoreboard players get #fgX mb
execute store result storage rlk:mboss fg.rd.len int 0.01 run scoreboard players get @s mbHzR
data modify storage rlk:mboss fg.rd merge value {w:24,back:0,el:9,hold:3}
execute rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/line with storage rlk:mboss fg.rd
