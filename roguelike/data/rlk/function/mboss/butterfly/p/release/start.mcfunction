# B5 달빛 해제 (service; clip release: cup 31, flash 35, glint 37, rings 38, wrap 44,
# detonation 53, shrink 87, shatter 91, land 96). The dome r 10 at R: 150 % Dendro.
# the release point R: L0 (the player's spot) + 4 b outward from the centre (from her when L0 is on the centre),
# pulled inside r 16; the fold fx (lime butterfly glyphs, a rim glow) and the swoop recipe
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p15l]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p15r]
function rlk:mboss/butterfly/rig/face/player
function rlk:mboss/butterfly/wx/u/lockw
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p15l]
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p15l
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p15l] add rlk_mb_bf_kept
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p15l] remove rlk_mb_bf_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15l,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p15","rlk_mb_bf_p15r","rlk_mb_bf_kept"]}
scoreboard players set #bp15C mb 0
execute at @e[tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_bf_p15l,distance=..1] run scoreboard players set #bp15C mb 1
execute if score #bp15C mb matches 0 as @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~180 0 run tp @s ^ ^ ^4
execute if score #bp15C mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~180 0 run tp @s ^ ^ ^4
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] at @s run tp @s ~ 201 ~
# a player beyond about r 12: the r 16 clamp would pull R back onto them (escape up to 10.3 b): R goes
# 4 b along the wall instead, on the side away from her (plan "Review-fix decisions", fairness F3: escape <= 6.5 b)
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] at @s unless entity @e[tag=rlk_mb_arena,distance=..16,limit=1] run function rlk:mboss/butterfly/p/release/tangent
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_r
function rlk:mboss/butterfly/p/release/swoop_t
execute rotated as @s rotated ~ 0 positioned ^0 ^3.175 ^0.447 run function rlk:mboss/butterfly/fx/p/rel_fold
execute rotated as @s rotated ~ 0 positioned ^0 ^3.175 ^0.447 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:1.6,move:"0f,0f,0f",life:10,fade:4,col:11985754}
function rlk:mboss/butterfly/fx/snd/release_swoop
