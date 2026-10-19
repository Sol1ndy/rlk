# @s = 몹, at @s. 지난 타격에서 예약된 반응(rxQ) 발동. 광역 피해는 여기서(최상위에서) 처리해 연쇄 반응이 꼬이지 않게 함
# 공격 순번(챕터 보스 히트 프록시의 중복 거름, mboss/px/hit)
scoreboard players add #atkSeq tmp 1
scoreboard players operation #q tmp = @s rxQ
scoreboard players operation #qDmg tmp = @s rxDmg
scoreboard players operation #qDmg3 tmp = @s rxDmg3
scoreboard players operation #qEl tmp = @s rxEl
scoreboard players set @s rxQ 0
execute if score #q tmp matches 3 run function rlk:element/run/overload
execute if score #q tmp matches 4 run function rlk:element/run/supercond
execute if score #q tmp matches 7 run function rlk:element/run/shatter
execute if score #q tmp matches 8 run function rlk:element/run/swirl
execute if score #q tmp matches 9 run function rlk:element/run/crystal
execute if score #q tmp matches 11 run function rlk:element/run/bloom
execute if score #q tmp matches 17..23 run function rlk:element/void/run
