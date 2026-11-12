# x1.3 timers: one extra step on game ticks 0, 3 and 6 of every 10 (integer, deterministic)
execute store result score #eHz tmp run time query gametime
scoreboard players operation #eHz tmp %= #10 tmp
execute if score #eHz tmp matches 0 run scoreboard players set #eStep tmp 2
execute if score #eHz tmp matches 3 run scoreboard players set #eStep tmp 2
execute if score #eHz tmp matches 6 run scoreboard players set #eStep tmp 2
execute if score #eStep tmp matches 2 if score @s cmCd matches 1.. run scoreboard players remove @s cmCd 1
execute if score #eStep tmp matches 2 if score @s cmCd2 matches 1.. run scoreboard players remove @s cmCd2 1
