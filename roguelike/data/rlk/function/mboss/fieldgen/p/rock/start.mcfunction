# C6 파쇄 (clip tower_throw; @s = body): bursts [55, 61, 67, 73, 79, 85, 91, 97], throws [95, 103, 111, 119, 127], revert 142.
scoreboard players set #fq6Pz mb 0
scoreboard players set #fq6SH mb 0
execute store result score #fq6S mb run random value 0..1
execute if score #fq6S mb matches 0 run scoreboard players set #fq6S mb -1
execute at @s unless entity @e[tag=rlk_body,distance=..5] run function rlk:mboss/fieldgen/u/toward {d:0.2}
function rlk:mboss/fieldgen/rig_stub/face/track
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/dip
execute at @s rotated as @s rotated ~ 0 positioned ~ ~2.8 ~ run function rlk:mboss/fieldgen/fx/snd/dip
