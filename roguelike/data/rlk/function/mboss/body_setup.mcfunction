function rlk:mboss/body_tag with storage rlk:mboss cur
function rlk:room/mob_init
execute store result score #t mb run data get storage rlk:mboss cur.lvAdd
execute unless score #t mb matches 0 run scoreboard players operation @s mlv += #t mb
execute unless score #t mb matches 0 run function rlk:mob/level_apply
attribute @s minecraft:attack_damage base set 0
attribute @s minecraft:movement_speed base set 0
function rlk:mob/setup
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
execute store result storage rlk:mboss a.s double 0.01 run data get storage rlk:mboss cur.scale 100
function rlk:mboss/body_scale with storage rlk:mboss a
scoreboard players set @s mres 0
