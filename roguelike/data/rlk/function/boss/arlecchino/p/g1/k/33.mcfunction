# G1 pattern tick 33
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzBol mb 6
scoreboard players set #hzBack mb 140
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~0 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:140,w:30,tell:1,dmg:36}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/g1
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzBol mb 6
scoreboard players set #hzBack mb 140
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~90 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:140,w:30,tell:1,dmg:36}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/g1
execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1] at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @s positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] if block ~ ~ ~ #rlk:dash_pass if block ~ ~1 ~ #rlk:dash_pass run tp @s ~ ~ ~
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~0 0 positioned ^0.55 ^ ^2.9 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:18}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~0 0 positioned ^-0.5 ^ ^1.75 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:27}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~0 0 positioned ^0.05 ^ ^0.6 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:21}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~90 0 positioned ^0.55 ^ ^2.9 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:29}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~90 0 positioned ^-0.5 ^ ^1.75 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:22}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~90 0 positioned ^0.05 ^ ^0.6 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:17}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~180 0 positioned ^0.55 ^ ^2.9 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:20}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~180 0 positioned ^-0.5 ^ ^1.75 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:24}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~180 0 positioned ^0.05 ^ ^0.6 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:18}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~270 0 positioned ^0.55 ^ ^2.9 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:26}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~270 0 positioned ^-0.5 ^ ^1.75 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:19}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~270 0 positioned ^0.05 ^ ^0.6 positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..26.5] run function rlk:boss/arlecchino/fx/p/cross_thorns {h:29}
