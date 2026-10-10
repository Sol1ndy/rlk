# 방패 휘두르기 (@s = 두뇌): 앞 3.3칸
# A rush contact and its ending swing share one damage check; normal swings are independent.
scoreboard players set #shBashHit tmp 1
execute if score @s cmS matches 4 if entity @s[tag=rlk_sh_rhit] run scoreboard players set #shBashHit tmp 0
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 10
function rlk:cm/pose_s
function rlk:cm/swing
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^1.3 ^1.4 run particle minecraft:sweep_attack ~ ~ ~ 0.3 0.1 0.3 0 2
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^1.2 ^1.4 run particle minecraft:crit ~ ~ ~ 0.4 0.3 0.4 0.2 10
execute unless score #k98 snd matches 1 run function rlk:snd/f105
execute unless score #k99 snd matches 1 run function rlk:snd/f106
$scoreboard players operation #cmDmg tmp = #cmD_$(d) tmp
execute if score #shBashHit tmp matches 1 if entity @e[tag=rlk_body,distance=..3.3] run function rlk:cm/hit_me
