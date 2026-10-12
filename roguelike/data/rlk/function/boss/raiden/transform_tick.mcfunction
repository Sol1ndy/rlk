# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 30 at @s rotated as @s run function rlk:boss/raiden/transform_title
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/vfx/transform
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/hazard/create {shape:8,tell:30,damage:18,life:42}
execute if score @s rdTime matches 15 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.3
execute if score @s rdTime matches 52 at @s rotated as @s run function rlk:boss/raiden/armor_start
