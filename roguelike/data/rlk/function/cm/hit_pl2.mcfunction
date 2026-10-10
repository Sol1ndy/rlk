scoreboard players operation @s hurtLv = #cmLv tmp
scoreboard players operation @s hurtElem = #cmEl tmp
scoreboard players operation #dmgIn tmp = #cmDmg tmp
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.62 ~ run function rlk:player/take_damage
execute if score #dodged tmp matches 1 run return 0
execute if score #cmKB tmp matches 1.. if entity @e[tag=rlk_plkb_source,limit=1] run function rlk:player/knockback/start
execute as @e[tag=rlk_body,limit=1] at @s run function rlk:cm/hurt_fx
