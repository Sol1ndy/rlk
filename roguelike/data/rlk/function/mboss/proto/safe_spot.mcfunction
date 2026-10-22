# Whole-arena blast with one safe circle (r 4.5) at a random spot within 12 blocks of the centre.
kill @e[tag=rlk_mb_proto_safe]
execute at @e[tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_proto_safe"]}
execute store result score #t mb run random value -120..120
execute store result score #t2 mb run data get entity @e[tag=rlk_mb_arena,limit=1] Pos[0] 10
scoreboard players operation #t mb += #t2 mb
execute store result entity @e[tag=rlk_mb_proto_safe,limit=1] Pos[0] double 0.1 run scoreboard players get #t mb
execute store result score #t mb run random value -120..120
execute store result score #t2 mb run data get entity @e[tag=rlk_mb_arena,limit=1] Pos[2] 10
scoreboard players operation #t mb += #t2 mb
execute store result entity @e[tag=rlk_mb_proto_safe,limit=1] Pos[2] double 0.1 run scoreboard players get #t mb
scoreboard players set #hzR0 mb 45
scoreboard players set #hzSfx mb 4
execute at @e[tag=rlk_mb_proto_safe,limit=1] run function rlk:mboss/hz/full {tell:44,dmg:140}
