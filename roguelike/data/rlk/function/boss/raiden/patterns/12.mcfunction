# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players operation @s rdRigL = @s rdAnim
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_summon
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/prison
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/fx/crystal
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/fx/snd/clap_summon
execute if score @s rdTime matches ..3 run return 0
execute if score @s rdTime matches 4 at @s rotated as @s run function rlk:boss/raiden/tm/clap/sphere
execute if score @s rdTime matches 16 at @s rotated as @s run function rlk:boss/raiden/tm/clap/orb
execute if score @s rdTime matches 17 at @s rotated as @s run execute as @e[tag=rlk_rd_tm_orb] at @e[tag=rlk_body,limit=1] run tp @s ~ ~1 ~
execute if score @s rdTime matches 24 at @s rotated as @s run kill @e[tag=rlk_rd_tm_orb]
execute if score @s rdTime matches 24 at @s rotated as @s run function rlk:boss/raiden/tm/clap/spawn
execute if score @s rdTime matches 25..49 at @s rotated as @s run function rlk:boss/raiden/tm/clap/follow
execute if score @s rdTime matches ..49 run return 0
execute if score @s rdTime matches 50 at @s rotated as @s run function rlk:boss/raiden/tm/clap/lock
execute if score @s rdTime matches 61 at @s rotated as @s run function rlk:boss/raiden/tm/clap/shut
execute if score @s rdTime matches 64 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_clapc,limit=1] run function rlk:boss/raiden/fx/snd/clap
execute if score @s rdTime matches 66 at @s rotated as @s run function rlk:boss/raiden/tm/clap/fade
execute if score @s rdTime matches 72 at @s rotated as @s run kill @e[tag=rlk_rd_clap]
execute if score @s rdTime matches 80 at @s rotated as @s run kill @e[tag=rlk_rd_tm_orb]
execute if score @s rdTime matches 80 at @s rotated as @s run function rlk:boss/raiden/tm/clap/spawn
execute if score @s rdTime matches ..80 run return 0
execute if score @s rdTime matches 81..103 at @s rotated as @s run function rlk:boss/raiden/tm/clap/follow
execute if score @s rdTime matches 104 at @s rotated as @s run function rlk:boss/raiden/tm/clap/lock
execute if score @s rdTime matches 115 at @s rotated as @s run function rlk:boss/raiden/tm/clap/shut
execute if score @s rdTime matches 118 at @s rotated as @s run execute at @e[tag=rlk_rd_tm_clapc,limit=1] run function rlk:boss/raiden/fx/snd/clap
execute if score @s rdTime matches 120 at @s rotated as @s run function rlk:boss/raiden/tm/clap/fade
execute if score @s rdTime matches 126 at @s rotated as @s run kill @e[tag=rlk_rd_clap]
execute if score @s rdTime matches ..129 run return 0
execute if score @s rdTime matches 130 at @s rotated as @s run function rlk:boss/raiden/finish
