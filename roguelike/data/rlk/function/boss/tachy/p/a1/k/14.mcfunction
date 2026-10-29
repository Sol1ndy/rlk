# A1 pattern tick 14
function rlk:boss/tachy/rig_stub/look/chest/off
scoreboard players operation #hzSzR mb = #a1_dl tk
scoreboard players set #t3 tk 5
scoreboard players operation #hzSzR mb *= #t3 tk
scoreboard players set #t3 tk 6
scoreboard players operation #hzSzR mb /= #t3 tk
execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag=rlk_tk_p_a1] run function rlk:boss/tachy/core/dash/grow
execute if score #a1_dl tk matches 0..8 if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #a1_dl tk matches 0..8 if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #a1_dl tk matches 9..16 if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #a1_dl tk matches 9..16 if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #a1_dl tk matches 17..24 if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #a1_dl tk matches 17..24 if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
