# @s = a quiet hazard marker in its tell, at / rotated as it: its kit decal again, from its scores (tenths of a block,
# the element colour mbHzE; hold 3). The resume hook runs before this tick's hz/all, which still counts mbHzT up
# once: the strike comes mbHzW - mbHzT - 1 ticks from now, the decal's tell. Storage rlk:mboss bfr = the macro args.
scoreboard players operation #bfX mb = @s mbHzW
scoreboard players operation #bfX mb -= @s mbHzT
scoreboard players remove #bfX mb 1
execute if score #bfX mb matches ..0 run return 0
execute store result storage rlk:mboss bfr.tell int 1 run scoreboard players get #bfX mb
execute store result storage rlk:mboss bfr.el int 1 run scoreboard players get @s mbHzE
data modify storage rlk:mboss bfr.hold set value 3
execute store result storage rlk:mboss bfr.r int 0.01 run scoreboard players get @s mbHzR
execute store result storage rlk:mboss bfr.r0 int 0.01 run scoreboard players get @s mbHzR0
execute store result storage rlk:mboss bfr.a int 1 run scoreboard players get @s mbHzAng
execute store result storage rlk:mboss bfr.len int 0.01 run scoreboard players get @s mbHzR
execute store result storage rlk:mboss bfr.w int 0.02 run scoreboard players get @s mbHzC
execute store result storage rlk:mboss bfr.back int 0.01 run scoreboard players get @s mbHzR0
execute if score @s mbHzK matches 1 run return run function rlk:mboss/butterfly/fx/tele/disc with storage rlk:mboss bfr
execute if score @s mbHzK matches 2 run return run function rlk:mboss/butterfly/fx/tele/ring with storage rlk:mboss bfr
execute if score @s mbHzK matches 3 run return run function rlk:mboss/butterfly/fx/tele/sector with storage rlk:mboss bfr
execute if score @s mbHzK matches 4 run return run function rlk:mboss/butterfly/fx/tele/line with storage rlk:mboss bfr
