# @s = 몹, at @s. 클릭 실드(인터랙션) 생성/추적/동기화 표시
# msid 부여
execute unless score @s msid matches 1.. run scoreboard players add #msidC tmp 1
execute unless score @s msid matches 1.. run scoreboard players operation @s msid = #msidC tmp
scoreboard players operation #mymid tmp = @s msid
# 내 실드 존재?
scoreboard players set #hasSh tmp 0
execute as @e[tag=rlk_mshield,distance=..24] if score @s msid = #mymid tmp run scoreboard players set #hasSh tmp 1
# 없으면 생성
execute if score #hasSh tmp matches 0 run summon minecraft:interaction ~ ~ ~ {Tags:["rlk_mshield","rlk_mshield_new"],width:1.2f,height:2.2f,response:false}
execute if score #hasSh tmp matches 0 run scoreboard players operation @e[tag=rlk_mshield_new,limit=1] msid = #mymid tmp
execute if score #hasSh tmp matches 0 run tag @e[tag=rlk_mshield_new] remove rlk_mshield_new
# 몹 위치로 tp + 생존 마킹
execute as @e[tag=rlk_mshield,distance=..24] if score @s msid = #mymid tmp run tp @s ~ ~ ~
execute as @e[tag=rlk_mshield,distance=..24] if score @s msid = #mymid tmp run tag @s add rlk_msync
