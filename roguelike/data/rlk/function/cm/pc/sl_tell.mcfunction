scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute store result score #c2t tmp run scoreboard players get @s cmT
scoreboard players operation #c2t tmp %= #2 tmp
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute if score #c2t tmp matches 0 rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^1 run function rlk:cm/pc/sl_ring
execute if score @s cmT matches ..0 run function rlk:cm/pc/sl_hit
