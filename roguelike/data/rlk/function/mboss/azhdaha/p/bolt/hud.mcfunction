# Every 2 t of a marker window: the chime when the player steps inside a safe circle.
execute if score #aq42J mb matches 3 run function rlk:mboss/azhdaha/p/bolt/dist_b
execute unless score #aq42J mb matches 3 run function rlk:mboss/azhdaha/p/bolt/dist_a
execute if score #aq42D mb = #aq42Dp mb run return 0
scoreboard players operation #aq42Dp mb = #aq42D mb
execute if score #aq42D mb matches 0 run function rlk:mboss/azhdaha/p/bolt/hud_in
execute if score #aq42D mb matches 1.. run scoreboard players set #aq42In mb 0
