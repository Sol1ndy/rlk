# 성동격서 (feint, id 6) - start (#azPT 0; feint: sways 0 / 12, burst 22). No decal (Change note 1): the sways are the tell
function rlk:mboss/grp_new
scoreboard players operation #aq6G mb = #mbGrp mb
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 4
scoreboard players set #hzKBDir mb 1
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
execute positioned ^2 ^0 ^-0.5 rotated ~-90 0 run function rlk:mboss/hz/line {len:66,w:110,tell:22,dmg:120}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p6
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p6h
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 4
scoreboard players set #hzKBDir mb 1
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
execute positioned ^-2 ^0 ^-0.5 rotated ~90 0 run function rlk:mboss/hz/line {len:66,w:110,tell:22,dmg:120}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p6
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p6h
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
execute positioned ^0 ^0 ^6.5 run function rlk:mboss/hz/disc {r:25,tell:22,dmg:60}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p6
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p6h
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
execute positioned ^0 ^0 ^-5.5 run function rlk:mboss/hz/disc {r:25,tell:22,dmg:60}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p6
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p6h
function rlk:mboss/azhdaha/fx/snd/feint_sway
execute positioned ^3.4 ^0 ^0 positioned ~ ~1.6 ~ run function rlk:mboss/azhdaha/fx/p/dust
execute positioned ^-3.4 ^0 ^0 positioned ~ ~1.6 ~ run function rlk:mboss/azhdaha/fx/p/dust
execute positioned ^3 ^0 ^-1.5 positioned ~ ~2.2 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.5 0.8 1.2 0 8 force @a[tag=player]
execute positioned ^3 ^0 ^1.5 positioned ~ ~2.2 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.5 0.8 1.2 0 8 force @a[tag=player]
execute positioned ^-3 ^0 ^-1.5 positioned ~ ~2.2 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.5 0.8 1.2 0 8 force @a[tag=player]
execute positioned ^-3 ^0 ^1.5 positioned ~ ~2.2 ~ run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~ ~ 0.5 0.8 1.2 0 8 force @a[tag=player]
