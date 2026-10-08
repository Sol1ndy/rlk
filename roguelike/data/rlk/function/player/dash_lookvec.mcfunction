# @s = 플레이어. 시선 방향 수평 전방 벡터를 #vx,#vz 에 (×100)
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_dashmk"]}
execute store result score #vx tmp run data get entity @e[tag=rlk_dashmk,limit=1] Pos[0] 100
execute store result score #vz tmp run data get entity @e[tag=rlk_dashmk,limit=1] Pos[2] 100
kill @e[tag=rlk_dashmk]
scoreboard players operation #vx tmp -= #cx tmp
scoreboard players operation #vz tmp -= #cz tmp
