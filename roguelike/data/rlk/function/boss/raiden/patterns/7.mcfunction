# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/calm
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/movement/blink_to
execute if score @s rdTime matches 1 at @s rotated as @s run playsound minecraft:entity.warden.sonic_charge hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.3
execute if score @s rdTime matches 10 at @s rotated as @s run scoreboard players set @s rdAnim 7
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/hazard/create {shape:14,tell:30,damage:30,life:40}
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 0 0 positioned ^ ^ ^21 run function rlk:boss/raiden/hazard/create {shape:3,tell:32,damage:10,life:42}
execute if score @s rdTime matches 10 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 0 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 45 0 positioned ^ ^ ^21 run function rlk:boss/raiden/hazard/create {shape:3,tell:30,damage:10,life:40}
execute if score @s rdTime matches 12 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 45 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score @s rdTime matches 14 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 90 0 positioned ^ ^ ^21 run function rlk:boss/raiden/hazard/create {shape:3,tell:28,damage:10,life:38}
execute if score @s rdTime matches 14 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 90 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score @s rdTime matches 16 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 135 0 positioned ^ ^ ^21 run function rlk:boss/raiden/hazard/create {shape:3,tell:26,damage:10,life:36}
execute if score @s rdTime matches 16 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 135 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score @s rdTime matches 18 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 180 0 positioned ^ ^ ^21 run function rlk:boss/raiden/hazard/create {shape:3,tell:24,damage:10,life:34}
execute if score @s rdTime matches 18 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 180 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score @s rdTime matches 20 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 225 0 positioned ^ ^ ^21 run function rlk:boss/raiden/hazard/create {shape:3,tell:22,damage:10,life:32}
execute if score @s rdTime matches 20 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 225 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score @s rdTime matches 22 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 270 0 positioned ^ ^ ^21 run function rlk:boss/raiden/hazard/create {shape:3,tell:20,damage:10,life:30}
execute if score @s rdTime matches 22 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 270 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score @s rdTime matches 24 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 315 0 positioned ^ ^ ^21 run function rlk:boss/raiden/hazard/create {shape:3,tell:18,damage:10,life:28}
execute if score @s rdTime matches 24 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute rotated 315 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score @s rdTime matches 38 at @s rotated as @s run function rlk:boss/raiden/line/sever_one
execute if score @s rdTime matches 40 at @s rotated as @s run playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.9 0.5 0.3
execute if score @s rdTime matches 39 at @s rotated as @s run scoreboard players set @s rdAnim 8
execute if score @s rdTime matches 42 at @s rotated as @s run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.9 0.85 0.3
execute if score @s rdTime matches 52 at @s rotated as @s run function rlk:boss/raiden/finish
