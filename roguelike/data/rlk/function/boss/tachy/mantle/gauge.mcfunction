# The mantle gauge on the HUD after a change (@s = body): kit gauge cells in 5 % steps, the cocoon cracks in 4.
scoreboard players operation #hud_g tk = #sh tk
execute if score #sh tk matches 76..1000 run scoreboard players set #hud_c tk 100
execute if score #sh tk matches 51..75 run scoreboard players set #hud_c tk 75
execute if score #sh tk matches 26..50 run scoreboard players set #hud_c tk 50
execute if score #sh tk matches -1000..25 run scoreboard players set #hud_c tk 25
