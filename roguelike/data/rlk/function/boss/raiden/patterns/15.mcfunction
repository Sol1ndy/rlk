# Pattern names intentionally stay out of the boss bar.
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/rig/start/t_vanish
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/line/mangeop
execute if score @s rdTime matches 1 at @s rotated as @s run scoreboard players set @s rdUltUsed 1
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdTime matches 1 at @s rotated as @s run execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdTime matches 1 at @s rotated as @s run function rlk:boss/raiden/fx/iai_charge
execute if score @s rdTime matches ..13 run return 0
execute if score @s rdTime matches 14 at @s rotated as @s run function rlk:boss/raiden/tm/mg/vanish
execute if score @s rdTime matches 18 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/mangeop_tint {life:160}
execute if score @s rdTime matches 40 at @s rotated as @s run function rlk:boss/raiden/tm/mg/flower
execute if score @s rdTime matches 42 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/danjeol_column
execute if score @s rdTime matches 56 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/raiden/judgment_rig/start
execute if score @s rdTime matches 56 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/snd/mangeop_rift
execute if score @s rdTime matches ..56 run return 0
execute if score @s rdTime matches 57..190 at @s rotated as @s run function rlk:boss/raiden/judgment_rig/tick
execute if score @s rdTime matches 74 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/snd/mangeop_void
execute if score @s rdTime matches 140 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/eye_spawn
execute if score @s rdTime matches 151 at @s rotated as @s run function rlk:boss/raiden/tm/mg/strike
execute if score @s rdTime matches 152 at @s rotated as @s run function rlk:boss/raiden/tm/mg/slash
execute if score @s rdTime matches 154 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~13 ~ ~-9 run function rlk:boss/raiden/fx/bolt_big
execute if score @s rdTime matches ..156 run return 0
execute if score @s rdTime matches 157 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-15 ~ ~4 run function rlk:boss/raiden/fx/bolt_big
execute if score @s rdTime matches 160 at @s rotated as @s run function rlk:boss/raiden/tm/mg/crack
execute if score @s rdTime matches 161 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~6 ~ ~16 run function rlk:boss/raiden/fx/bolt_big
execute if score @s rdTime matches 165 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-9 ~ ~-14 run function rlk:boss/raiden/fx/bolt_big
execute if score @s rdTime matches 176 at @s rotated as @s run function rlk:boss/raiden/tm/mg/shatter
execute if score @s rdTime matches 178 at @s rotated as @s run execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/snd/mangeop_close
execute if score @s rdTime matches ..183 run return 0
execute if score @s rdTime matches 184 at @s rotated as @s run function rlk:boss/raiden/tm/mg/reform
execute if score @s rdTime matches 196 at @s rotated as @s run function rlk:boss/raiden/finish
