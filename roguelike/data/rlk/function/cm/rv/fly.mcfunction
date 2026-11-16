# orbit point: 5.5 b from the body at 3 b over its feet, clamped into the box and under the ceiling
execute if score @s frzT matches 1.. run return 0
execute if score @s stunT matches 1.. run return 0
scoreboard players add @s c2eA 3
execute if score #eStep tmp matches 2 run scoreboard players add @s c2eA 3
execute if score @s c2eA matches 360.. run scoreboard players remove @s c2eA 360
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 1 run scoreboard players get @s c2eA
execute positioned as @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^5.5 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~
scoreboard players set #oUp tmp 300
function rlk:cm/rv/clamp
function rlk:cm/rv/step
execute if score #eStep tmp matches 2 at @s run function rlk:cm/rv/step
