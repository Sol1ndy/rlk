# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 12
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/clap/spawn
execute if score @s rdTime matches 1..16 run function rlk:boss/raiden/clap/follow
execute if score @s rdTime matches 17 at @s rotated as @s run function rlk:boss/raiden/clap/lock
execute if score @s rdTime matches 24 at @s rotated as @s run function rlk:boss/raiden/clap/shut
execute if score @s rdTime matches 24 at @s rotated as @s run scoreboard players set @s rdAnim 13
execute if score @s rdTime matches 27 at @s rotated as @s run playsound minecraft:entity.iron_golem.attack hostile @a[tag=player] ~ ~ ~ 1 0.65 0.3
execute if score @s rdTime matches 27 at @s rotated as @s run playsound minecraft:entity.zombie.attack_iron_door hostile @a[tag=player] ~ ~ ~ 0.7 0.6 0.3
execute if score @s rdTime matches 30 at @s rotated as @s run function rlk:boss/raiden/clap/fade
execute if score @s rdTime matches 36 at @s rotated as @s run function rlk:boss/raiden/clap/clear
execute if score @s rdTime matches 37 at @s rotated as @s run function rlk:boss/raiden/finish
