# Phase 1 (plan 7.3 / 7.4). Returns 1 when it picked. Anti-stall: BACK for >= 3 decisions while P5 cools down -> a
# 180-degree crab-turn. Rim: the anchor beyond r 12 with the player BACK -> P1 (50 %, off cooldown) or
# the turn. BACK rule: BACK for >= 2 of the last 3 samples -> 75 % P5 (off its cooldown).
execute unless score #apZone mb matches 4 run scoreboard players set #apBackN mb 0
execute unless score #apZone mb matches 4 run return fail
execute if score #apFc mb < #apCdE5 mb run scoreboard players add #apBackN mb 1
execute if score #apBackN mb matches 3.. run return run function rlk:mboss/apep/ai/turn180
execute if score #apRim mb matches 1 run return run function rlk:mboss/apep/ai/rim
execute if score #apBackT mb matches ..1 run return fail
execute store result score #apR mb run random value 0..99
execute if score #apR mb matches 75.. run return fail
execute if score #apFc mb < #apCdE5 mb run return fail
return run function rlk:mboss/apep/ai/back_p5
