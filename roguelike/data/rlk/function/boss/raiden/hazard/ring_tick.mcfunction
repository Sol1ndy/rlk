scoreboard players operation #rdElapsed rd = @s rdHAge
scoreboard players operation #rdElapsed rd -= @s rdWind
execute if score #rdElapsed rd matches 32.. run return run function rlk:boss/raiden/hazard/expire
execute unless score #rdElapsed rd matches 0..31 run return 0
# Every damage radius receives its matching model in the same tick.
function rlk:boss/raiden/hazard/ring_draw
execute if score #rdElapsed rd matches 0 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.2
execute unless score @s rdHHit matches 1 run function rlk:boss/raiden/hazard/hit
