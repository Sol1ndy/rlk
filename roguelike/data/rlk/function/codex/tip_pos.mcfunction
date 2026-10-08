scoreboard players operation #col tmp = @s pkHI
scoreboard players operation #col tmp %= #c8 tmp
execute if score @s pkHK matches 13 if score #col tmp matches ..3 at @s anchored eyes positioned ^-1.7 ^ ^3 run tp @e[tag=rlk_pk_tip] ~ ~ ~
execute if score @s pkHK matches 13 if score #col tmp matches 4.. at @s anchored eyes positioned ^1.7 ^ ^3 run tp @e[tag=rlk_pk_tip] ~ ~ ~
execute if score @s pkHK matches 13 if score #col tmp matches ..3 at @s anchored eyes positioned ^1.7 ^ ^3 run tp @e[tag=rlk_pk_tip2] ~ ~ ~
execute if score @s pkHK matches 13 if score #col tmp matches 4.. at @s anchored eyes positioned ^-1.7 ^ ^3 run tp @e[tag=rlk_pk_tip2] ~ ~ ~
