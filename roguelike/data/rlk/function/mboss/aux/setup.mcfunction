attribute @s minecraft:attack_damage base set 0
attribute @s minecraft:movement_speed base set 0
scoreboard players operation @s mlv = #mbLv mb
execute unless score @s mlv matches 1.. run scoreboard players set @s mlv 1
function rlk:mob/setup
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
execute if score #auxHpPct mb matches 1.. run function rlk:mboss/aux/pool_pct
scoreboard players operation @s mhpM = #auxHp mb
execute unless score @s mhpM matches 1.. run scoreboard players set @s mhpM 1
scoreboard players operation @s mhpC = @s mhpM
scoreboard players operation @s mres = #auxRes mb
execute if score #auxResEl mb matches 0..8 run function rlk:mboss/aux/res_el
