# @s = the dest marker, at it (rotation = toward the player): one 0.5 b step while allowed (#mbDist = the
# distance to the player from here, tenths). In butterfly form the point stays inside r 16.5 (plan Q9, fix S6).
execute if score #bfDLeft mb matches ..4 run return 0
scoreboard players remove #mbDist mb 5
execute if score #mbDist mb < #bfDKeep mb run return 0
execute rotated as @s positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0
execute if score #bfForm mb matches 2 rotated as @s positioned ^ ^ ^0.5 unless function rlk:mboss/butterfly/wx/u/okb run return 0
execute rotated as @s run tp @s ^ ^ ^0.5
scoreboard players remove #bfDLeft mb 5
execute at @s run function rlk:mboss/butterfly/u/dest_step
