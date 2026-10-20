# Every 2 t of a marker window: the sub-line part (rlk:mboss az.subx, s2.md 16) and the chime inside.
scoreboard players set #aq42D mb 99
execute if score #aq42J mb matches 3 run function rlk:mboss/azhdaha/p/bolt/dist_b
execute unless score #aq42J mb matches 3 run function rlk:mboss/azhdaha/p/bolt/dist_a
execute if score #aq42D mb = #aq42Dp mb run return 0
scoreboard players operation #aq42Dp mb = #aq42D mb
execute if score #aq42D mb matches 0 run function rlk:mboss/azhdaha/p/bolt/hud_in
execute if score #aq42D mb matches 1.. run function rlk:mboss/azhdaha/p/bolt/hud_out
scoreboard players set #azHudQ mb 1
