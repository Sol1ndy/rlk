# 근접 평타의 위치·수평 방향 저장. @s = 플레이어, 실행 위치·회전 = 몸.
# 전용 마커와 점수로 방패 흡수/피해 처리의 임시 값과 충돌하지 않는다.
# 공격 순번(챕터 보스 히트 프록시의 중복 거름, mboss/px/hit)
scoreboard players add #atkSeq tmp 1
kill @e[tag=rlk_melee_origin]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_melee_origin"]}
tp @e[tag=rlk_melee_origin,limit=1] ~ ~ ~ ~ 0
execute store result score #meleeYaw tmp run data get entity @e[tag=rlk_melee_origin,limit=1] Rotation[0] 100
scoreboard players set #meleeFront tmp 0
