# From room/zone_build (@s = the zone marker, after zst 1): the rift roll of PLAN §7.1. A forced rift (test/rift,
# rift_id, special) takes the next zone built of any kind but 9 (boss) / 15 (mid-boss), regardless of chance,
# #riftUsed, map type, chapter or test state. Naturally: a run, no boss test, no rift yet this run, a combat room
# (zkind 1), not the boss map, not chapter 1's first map, a special with w >= 1 enabled, not peaceful, then
# #riftPm per mille.
execute if score #riftForce room matches 1 unless score @s zkind matches 9 unless score @s zkind matches 15 run return run function rlk:room/rift/arm
execute unless score #active room matches 1 run return 0
execute if score #riftUsed room matches 1.. run return 0
execute unless score @s zkind matches 1 run return 0
execute if score #mapType room matches 8 run return 0
execute if score #chapter room matches 1 if score #mapIdx room matches 0 run return 0
execute if score #mbTest mb matches 1 run return 0
execute if score #rdTest rd matches 1 run return 0
execute unless score #spRoll mb matches 1.. run return 0
execute store result score #riftDiff room run difficulty
execute if score #riftDiff room matches 0 run return 0
execute store result score #riftR room run random value 0..999
execute if score #riftR room < #riftPm room run function rlk:room/rift/arm
