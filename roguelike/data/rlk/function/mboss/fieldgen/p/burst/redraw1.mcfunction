# @s = a quiet hazard marker, at it. The ticks to its strike are mbHzW - mbHzT - 1 in the module tick (hz/all
# advances mbHzT after it); the sizes come from its scores (milliblocks -> tenths of a block).
scoreboard players operation #fgX mb = @s mbHzW
scoreboard players operation #fgX mb -= @s mbHzT
scoreboard players remove #fgX mb 1
execute if score #fgX mb matches ..0 run return 0
execute store result storage rlk:mboss fg.rd.tell int 1 run scoreboard players get #fgX mb
execute store result storage rlk:mboss fg.rd.r int 0.01 run scoreboard players get @s mbHzR
execute store result storage rlk:mboss fg.rd.len int 0.01 run scoreboard players get @s mbHzR
execute store result storage rlk:mboss fg.rd.r0 int 0.01 run scoreboard players get @s mbHzR0
execute store result storage rlk:mboss fg.rd.back int 0.01 run scoreboard players get @s mbHzR0
execute store result storage rlk:mboss fg.rd.w int 0.02 run scoreboard players get @s mbHzC
data modify storage rlk:mboss fg.rd merge value {el:5,hold:3}
execute if score @s mbHzK matches 1 rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/disc with storage rlk:mboss fg.rd
execute if score @s mbHzK matches 2 rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/ring with storage rlk:mboss fg.rd
execute if score @s mbHzK matches 4 rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/fx/tele/line with storage rlk:mboss fg.rd
