# Short strafing steps: 16 t of every 40 t (fight clock), alternating sides.
scoreboard players operation #bfM mb = #bfClk mb
scoreboard players operation #bfM mb %= #bfK40 mb
execute if score #bfM mb matches 0 run scoreboard players operation #bfSide mb *= #cm1 mb
execute if score #bfM mb matches 0..15 run return run function rlk:mboss/butterfly/ai/strafe_go
execute unless score #bfMv mb matches 0 run function rlk:mboss/butterfly/ai/mv0
