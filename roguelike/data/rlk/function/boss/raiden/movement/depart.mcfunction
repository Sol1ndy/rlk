# Pure art helper: as the boss (or a clone husk) at @s, its yaw; never moves her or changes rdBlink.
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/movement/art {kind:1,model:"tenma_0"}
execute unless score @s rdPhase matches 2 run function rlk:boss/raiden/movement/art {kind:1,model:"shogun_0"}
playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~1 ~ 0.6 1.45 0.15
