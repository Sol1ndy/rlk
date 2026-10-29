execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^1.3 if entity @e[tag=rlk_body,distance=..1.6] run function rlk:cm/cs/p_dmg2
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^-0.5 ^1 ^1.6 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
playsound minecraft:entity.player.attack.strong master @a ~ ~ ~ 0.8 0.7
scoreboard players set @s cmS 7
scoreboard players set @s cmT 10
tag @s remove rlk_cmch
scoreboard players set @s cmCd 46
