# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# Every 8 t: the next wave is due when <= 1 organisms are alive (pending spawns count) or 600 t after the last;
# it waits while alive + its size > the cap 6 (the time-out spawns ignore the cap).
execute store result score #apAlive mb if entity @e[type=minecraft:husk,tag=rlk_mb_ap_org,tag=!rlk_mb_ap_dying]
execute store result score #apX mb if entity @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn]
scoreboard players operation #apAlive mb += #apX mb
scoreboard players set #apX mb 0
execute if score #apWT mb matches 600.. run scoreboard players set #apX mb 1
execute if score #apAlive mb matches ..1 run scoreboard players set #apX mb 1
execute if score #apX mb matches 0 run return 0
scoreboard players set #apY mb 4
execute if score #apWave mb matches 1.. run scoreboard players set #apY mb 5
execute if score #apWave mb matches 6.. run scoreboard players set #apY mb 6
scoreboard players operation #apY mb += #apAlive mb
execute if score #apY mb matches 7.. run return 0
function rlk:boss/apep/rev/wave_go
