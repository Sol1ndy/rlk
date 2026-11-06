# Sheathed locomotion: weapon on the back, relaxed empty-hand arms.
execute if score @s pmWantMode matches 0 run data modify storage rlk:player_motion loco.mode set value "idle_s"
execute if score @s pmWantMode matches 1 run data modify storage rlk:player_motion loco.mode set value "walk_s"
execute if score @s pmWantMode matches 2 run data modify storage rlk:player_motion loco.mode set value "run_s"
execute if score @s pmWantMode matches 3 run data modify storage rlk:player_motion loco.mode set value "air_s"
