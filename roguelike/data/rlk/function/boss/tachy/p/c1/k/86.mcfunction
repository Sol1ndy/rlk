# C1 pattern tick 86
scoreboard players operation #hzSzR mb = #c1_dl tk
scoreboard players set #t3 tk 5
scoreboard players operation #hzSzR mb *= #t3 tk
scoreboard players set #t3 tk 4
scoreboard players operation #hzSzR mb /= #t3 tk
execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag=rlk_tk_p_c1] run function rlk:boss/tachy/core/dash/grow
execute if score #c1_dl tk matches 0..4 if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #c1_dl tk matches 0..4 if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #c1_dl tk matches 5..9 if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #c1_dl tk matches 5..9 if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #c1_dl tk matches 10..14 if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
execute if score #c1_dl tk matches 10..14 if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]
playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
function rlk:boss/tachy/el/edge
