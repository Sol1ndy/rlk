scoreboard players set @s cmS 0
scoreboard players set @s cmAR 11
function rlk:cm/pose_s
function rlk:cm/swing
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^1.1 ^1.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1
execute unless score #k104 snd matches 1 run function rlk:snd/f111
scoreboard players operation #cmDmg tmp = #cmD_sw tmp
execute if entity @e[tag=rlk_body,distance=..3.0] run function rlk:cm/hit_me
