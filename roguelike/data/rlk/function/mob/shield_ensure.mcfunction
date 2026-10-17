execute if entity @s[tag=rlk_raiden,scores={rdPat=5}] run return 0
execute if entity @s[tag=rlk_raiden,scores={rdDeath=1}] run return 0
execute if entity @s[tag=rlk_raiden,scores={rdBlink=1..}] run return 0
execute if entity @s[tag=rlk_raiden,scores={rdPat=15}] run return 0
# 중간보스 무적(등장 · 쓰러짐 · 모듈의 무적 동작): 클릭 실드 없음
execute if entity @s[tag=rlk_mb_inv] run return 0
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
execute if score #hasSh tmp matches 0 if entity @s[tag=rlk_cmbig] run data merge entity @e[tag=rlk_mshield_new,limit=1] {width:1.5f,height:2.7f}
# 중간보스 몸체: 레지스트리 hit {w,h}
execute if score #hasSh tmp matches 0 if entity @s[tag=rlk_mb_body] run function rlk:mboss/shield_size with storage rlk:mboss cur.hit
execute if score #hasSh tmp matches 0 run tag @e[tag=rlk_mshield_new] remove rlk_mshield_new
# 몹 위치로 tp + 생존 마킹
execute as @e[tag=rlk_mshield,distance=..24] if score @s msid = #mymid tmp run tp @s ~ ~ ~
execute as @e[tag=rlk_mshield,distance=..24] if score @s msid = #mymid tmp run tag @s add rlk_msync
# 나루카미: 공중에 떠오른 변신 몸체까지 클릭 판정을 맞춘다.
execute if entity @s[tag=rlk_raiden] unless score @s rdPhase matches 2 as @e[tag=rlk_mshield,distance=..24] if score @s msid = #mymid tmp unless data entity @s {width:1.4f,height:2.6f} run data merge entity @s {width:1.4f,height:2.6f}
execute if entity @s[tag=rlk_raiden] if score @s rdPhase matches 2 as @e[tag=rlk_mshield,distance=..24] if score @s msid = #mymid tmp unless data entity @s {width:1.8f,height:4.5f} run data merge entity @s {width:1.8f,height:4.5f}
