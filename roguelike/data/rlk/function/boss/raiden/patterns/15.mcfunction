# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/judgment_start
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdAnim 16
execute if score @s rdTime matches 2..25 at @s run tp @s ~ ~0.32 ~
execute if score @s rdTime matches 3 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~9 ~ ~-6 run function rlk:boss/raiden/vfx/judgment_bolt
execute if score @s rdTime matches 3 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~9 ~ ~-6 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 1.2 0.7 0.4
execute if score @s rdTime matches 7 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-11 ~ ~4 run function rlk:boss/raiden/vfx/judgment_bolt
execute if score @s rdTime matches 7 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-11 ~ ~4 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 1.2 0.7 0.4
execute if score @s rdTime matches 11 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~5 ~ ~12 run function rlk:boss/raiden/vfx/judgment_bolt
execute if score @s rdTime matches 11 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~5 ~ ~12 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 1.2 0.7 0.4
execute if score @s rdTime matches 15 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-7 ~ ~-12 run function rlk:boss/raiden/vfx/judgment_bolt
execute if score @s rdTime matches 15 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-7 ~ ~-12 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 1.2 0.7 0.4
execute if score @s rdTime matches 19 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~13 ~ ~6 run function rlk:boss/raiden/vfx/judgment_bolt
execute if score @s rdTime matches 19 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~13 ~ ~6 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 1.2 0.7 0.4
execute if score @s rdTime matches 23 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-14 ~ ~-3 run function rlk:boss/raiden/vfx/judgment_bolt
execute if score @s rdTime matches 23 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-14 ~ ~-3 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 1.2 0.7 0.4
execute if score @s rdTime matches 26 at @s rotated as @s run function rlk:boss/raiden/movement/depart
execute if score @s rdTime matches 26 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 1 0.6 0.3
execute if score @s rdTime matches 26 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~ ~ ~-8 run tp @s ~ ~ ~ 0 0
execute if score @s rdTime matches 47 at @s rotated as @s run function rlk:boss/raiden/judgment_hint
execute if score @s rdTime matches 30 at @s rotated as @s run playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.6 0.5 0.3
execute if score @s rdTime matches 70 at @s rotated as @s run playsound minecraft:block.portal.ambient hostile @a[tag=player] ~ ~ ~ 0.45 0.55 0.3
execute if score @s rdTime matches 120 at @s rotated as @s run function rlk:boss/raiden/judgment_strike
execute if score @s rdTime matches 170 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 170 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 170 at @s rotated as @s run function rlk:boss/raiden/movement/arrive
execute if score @s rdTime matches 176 at @s rotated as @s run function rlk:boss/raiden/finish
