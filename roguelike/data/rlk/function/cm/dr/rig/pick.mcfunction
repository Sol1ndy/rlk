scoreboard players operation #pose tmp = @s cmAF
scoreboard players operation #pose tmp /= #c2c12 tmp
execute if entity @s[tag=rlk_dr_drum] if score @s c2T matches 0..1 run scoreboard players set #pose tmp 61
execute if entity @s[tag=rlk_dr_drum] if score @s c2T matches 2..7 run scoreboard players set #pose tmp 62
execute if entity @s[tag=rlk_dr_drum] if score @s c2T matches 8..9 run scoreboard players set #pose tmp 63
execute if entity @s[tag=rlk_dr_drum] if score @s c2T matches 10.. run scoreboard players set #pose tmp 60
execute if score @s c2T2 matches 1.. run scoreboard players set #pose tmp 70
execute if score @s cmAH matches 4.. run scoreboard players set #pose tmp 40
