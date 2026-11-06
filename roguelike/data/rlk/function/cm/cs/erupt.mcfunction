# surfaces right here (a walked safe column) with an uppercut; then stuck in the sand: the punish window
function rlk:cm/cs/surface
execute if entity @e[tag=rlk_body,distance=..1.8] run function rlk:cm/cs/e_dmg
particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.6 ~ 0.9 0.6 0.9 0.15 70
particle minecraft:poof ~ ~0.5 ~ 0.7 0.3 0.7 0.05 16
particle minecraft:electric_spark ~ ~1.2 ~ 0.4 0.6 0.4 0.1 12
playsound minecraft:entity.warden.emerge master @a ~ ~ ~ 0.8 1.6
playsound minecraft:entity.player.attack.knockback master @a ~ ~ ~ 1 0.6
scoreboard players set @s cmS 4
scoreboard players set @s cmT 24
scoreboard players set @s cmCd2 150
execute if score @s cmCd matches ..29 run scoreboard players set @s cmCd 30
