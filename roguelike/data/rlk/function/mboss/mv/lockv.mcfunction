# {lead} (as anything; cm.md 13.1): v = (newest - oldest) / 5 of the ring buffer in mb/t, |v| capped at 280 (sprint):
# #mbVx #mbVz = v, #mbV = |v|; the old rlk_mb_lock marker dies and a new one (rlk_room rlk_mb_aux rlk_mb_lock) stands at
# the player + v x lead, y = the arena centre, pulled inside walk - 0.7 (ar/clampw). A module that keeps the marker
# removes rlk_mb_lock from it (the next lockv kills a tagged one).
execute unless function rlk:mboss/mv/plpos run return fail
scoreboard players operation #lx mb = #mbPX mb
scoreboard players operation #lz mb = #mbPZ mb
execute unless data storage rlk:mboss lv[5] run function rlk:mboss/mv/lv_fill
execute store result score #mbVx mb run data get storage rlk:mboss lv[5].x
execute store result score #t mb run data get storage rlk:mboss lv[0].x
scoreboard players operation #mbVx mb -= #t mb
scoreboard players set #t mb 5
scoreboard players operation #mbVx mb /= #t mb
execute store result score #mbVz mb run data get storage rlk:mboss lv[5].z
execute store result score #t mb run data get storage rlk:mboss lv[0].z
scoreboard players operation #mbVz mb -= #t mb
scoreboard players set #t mb 5
scoreboard players operation #mbVz mb /= #t mb
# |v| (integer Newton square root; a teleport-sized jump is clamped before squaring)
execute if score #mbVx mb matches 20001.. run scoreboard players set #mbVx mb 20000
execute if score #mbVx mb matches ..-20001 run scoreboard players set #mbVx mb -20000
execute if score #mbVz mb matches 20001.. run scoreboard players set #mbVz mb 20000
execute if score #mbVz mb matches ..-20001 run scoreboard players set #mbVz mb -20000
scoreboard players operation #n mb = #mbVx mb
scoreboard players operation #n mb *= #mbVx mb
scoreboard players operation #t mb = #mbVz mb
scoreboard players operation #t mb *= #mbVz mb
scoreboard players operation #n mb += #t mb
scoreboard players set #mbV mb 0
execute if score #n mb matches 1.. run function rlk:mboss/mv/lv_sqrt
execute if score #mbV mb matches 281.. run function rlk:mboss/mv/lv_cap
# lock point = the player + v x lead (milliblocks), y = the arena centre
$scoreboard players set #t mb $(lead)
scoreboard players operation #lx2 mb = #mbVx mb
scoreboard players operation #lx2 mb *= #t mb
scoreboard players operation #lx2 mb += #lx mb
scoreboard players operation #lz2 mb = #mbVz mb
scoreboard players operation #lz2 mb *= #t mb
scoreboard players operation #lz2 mb += #lz mb
kill @e[type=minecraft:marker,tag=rlk_mb_lock]
execute at @e[tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_lock","rlk_mb_locknew"]}
execute store result entity @e[type=minecraft:marker,tag=rlk_mb_locknew,limit=1] Pos[0] double 0.001 run scoreboard players get #lx2 mb
execute store result entity @e[type=minecraft:marker,tag=rlk_mb_locknew,limit=1] Pos[2] double 0.001 run scoreboard players get #lz2 mb
execute as @e[type=minecraft:marker,tag=rlk_mb_locknew,limit=1] run function rlk:mboss/ar/clampw
tag @e[type=minecraft:marker,tag=rlk_mb_locknew] remove rlk_mb_locknew
return 1
