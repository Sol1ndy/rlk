execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
scoreboard players set #c2h tmp 0
scoreboard players set #n tmp 7
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^0.9 ^0.6 run function rlk:cm/cs/t_ray
execute if score #c2h tmp matches 1 run function rlk:cm/cs/t_dmg
playsound minecraft:item.trident.hit master @a ~ ~ ~ 1 0.7
playsound minecraft:entity.lightning_bolt.impact master @a ~ ~ ~ 0.4 1.8
scoreboard players set @s cmS 9
scoreboard players set @s cmT 12
tag @s remove rlk_cmch
scoreboard players set @s cmCd 46
