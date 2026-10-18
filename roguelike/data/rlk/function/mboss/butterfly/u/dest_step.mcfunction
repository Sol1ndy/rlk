# @s = the dest marker, at it (rotation = toward the player): one 0.5 b step while allowed.
execute if score #bfDLeft mb matches ..4 run return 0
function rlk:mboss/mv/dist
scoreboard players remove #mbDist mb 5
execute if score #mbDist mb < #bfDKeep mb run return 0
execute rotated as @s positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0
execute rotated as @s run tp @s ^ ^ ^0.5
scoreboard players remove #bfDLeft mb 5
execute at @s run function rlk:mboss/butterfly/u/dest_step
