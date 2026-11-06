# Pure art helper: as the boss (or a clone husk) at @s, its yaw; never moves her or changes rdBlink.
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/movement/art {kind:2,model:"tenma_5"}
execute unless score @s rdPhase matches 2 run function rlk:boss/raiden/movement/art {kind:2,model:"shogun_5"}
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~1 ~ 0.22 1.75 0.1
