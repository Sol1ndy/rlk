# Pure VFX helper: call as boss at @s; never moves the boss or changes rdBlink.
# Reused by the ultimate disappearance/return independently of ordinary blink.
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/movement/arrive_armored
execute unless score @s rdPhase matches 2 run function rlk:boss/raiden/movement/arrive_normal
