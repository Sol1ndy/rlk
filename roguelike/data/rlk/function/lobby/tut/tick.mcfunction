# 튜토리얼 (@s = 플레이어)
# 2단계: 허수아비가 쓰러졌으면 완료
execute if score #tutS lob matches 2 if score #tutW lob matches 0 if score #tutC lob matches 0 unless entity @e[tag=rlk_tutT,limit=1] run scoreboard players set #tutC lob 1
# 7단계: 더미에 원소를 다시 붙임(2초마다)
execute if score #tutS lob matches 7 store result score #t lob run time query gametime
execute if score #tutS lob matches 7 run scoreboard players operation #t lob %= #c40 lob
execute if score #tutS lob matches 7 if score #t lob matches 0 run function rlk:lobby/tut/aura
# 8단계 · 캐릭터 3쪽(23): 쓸 때까지 에너지 가득
execute if score #tutS lob matches 8 if score #tutW lob matches 0 run scoreboard players operation @s energy = #burstCost100 tmp
execute if score #tutS lob matches 23 if score #tutW lob matches 0 run scoreboard players operation @s energy = #burstCost100 tmp
execute if score #tutS lob matches 23 if score #tutW lob matches 0 run scoreboard players set @s burstCd 0
# 캐릭터 2쪽(22): 스킬을 바로 다시 쓸 수 있게
execute if score #tutS lob matches 22 if score #tutW lob matches 0 run scoreboard players set @s skillCd 0
execute if score #tutS lob matches 22 if score #tutW lob matches 0 if score #charN tmp matches 8 run scoreboard players set @s nfC 2
# 진행 표시 · 완료
execute unless score #tutC lob = #tutCp lob run function rlk:lobby/tut/goal
execute if score #tutW lob matches 0 if score #tutNeed lob matches 1.. if score #tutC lob >= #tutNeed lob run function rlk:lobby/tut/done
execute if score #tutW lob matches 1.. run scoreboard players remove #tutW lob 1
execute if score #tutW lob matches 1 run function rlk:lobby/tut/next
