# @s = the zone marker, at it: up to 24 random cell points of the zone (as room/mob_try), the ground found as
# room/mob_up; accepted when spot/check passes. Fallback: the zone centre ground, then 2 b in front of the player's
# rlk_safe spot. Result: one marker rlk_riftc at the spot, #riftWay room = 1 random / 2 centre / 3 safe / 0 none;
# the zone is tagged rlk_riftcz (the anchor turns toward it).
tag @s add rlk_riftcz
scoreboard players set #riftTry room 0
scoreboard players set #riftWay room 0
scoreboard players set #riftCr room 0
execute if score @s zkind matches 4 run scoreboard players set #riftCr room 8100
execute if score #riftCr room matches 0 unless score @s zkind matches 0..1 run scoreboard players set #riftCr room 2025
execute store result score #riftCx room run data get entity @s Pos[0] 10
execute store result score #riftCz room run data get entity @s Pos[2] 10
function rlk:room/rift/spot/try
execute if score #riftWay room matches 0 positioned ~0.5 ~ ~0.5 run function rlk:room/rift/spot/centre
execute if score #riftWay room matches 0 run function rlk:room/rift/spot/safe
