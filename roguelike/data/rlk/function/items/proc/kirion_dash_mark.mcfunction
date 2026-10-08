# @s = 플레이어, at @s. 현재 지점에 참격 마커 (6틱 뒤 그 자리에서 참격 발동)
summon minecraft:marker ~ ~1 ~ {Tags:["rlk_kslash","rlk_kslash_new"]}
data modify entity @e[tag=rlk_kslash_new,limit=1] Rotation set from entity @e[tag=rlk_body,limit=1] Rotation
scoreboard players set @e[tag=rlk_kslash_new,limit=1] life 6
tag @e[tag=rlk_kslash_new] remove rlk_kslash_new
