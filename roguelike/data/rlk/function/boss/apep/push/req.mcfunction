# @s = body: the body push request (FN-21, cm.md 13.5; #mbPushOn is a per-tick request): only in the rest sets p1 /
# p3u / p3c, the anchor moved <= 0.15 b/t and turned <= 6 deg/t since the last tick, no pattern request #apNoPush,
# no Q2 dome round (rlk_mb_hzsafe markers).
scoreboard players set #apMov mb 0
execute store result score #apX mb run data get entity @s Pos[0] 1000
execute store result score #apZ mb run data get entity @s Pos[2] 1000
execute store result score #apY mb run data get entity @s Rotation[0] 100
scoreboard players operation #apDX mb = #apX mb
scoreboard players operation #apDX mb -= #apLX mb
scoreboard players operation #apDZ mb = #apZ mb
scoreboard players operation #apDZ mb -= #apLZ mb
scoreboard players operation #apDY mb = #apY mb
scoreboard players operation #apDY mb -= #apLY mb
execute unless score #apDX mb matches -150..150 run scoreboard players set #apMov mb 1
execute unless score #apDZ mb matches -150..150 run scoreboard players set #apMov mb 1
execute unless score #apDY mb matches -600..600 run scoreboard players set #apMov mb 1
scoreboard players operation #apLX mb = #apX mb
scoreboard players operation #apLZ mb = #apZ mb
scoreboard players operation #apLY mb = #apY mb
execute unless score #apPx mb matches 0..2 run return 0
execute if score #apMov mb matches 1 run return 0
execute if score #apNoPush mb matches 1 run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_mb_hzsafe,limit=1] run return 0
scoreboard players set #mbPushOn mb 1
