# 로비 시스템 매 틱 (루트 tick 의 맨 끝)
# 방 짓기: 판 번호(built)가 다르면 다시 짓는다 (청크가 불러와졌을 때)
execute unless data storage rlk:lobby {built:11} in minecraft:overworld if loaded 80 192 14 if loaded 106 192 36 if loaded 134 192 16 if loaded 134 192 64 if loaded 92 192 50 run function rlk:lobby/build
# 접속 처리
execute as @a[tag=!rlk_seen] run function rlk:lobby/first
execute as @a[scores={rlkLeave=1..}] run function rlk:lobby/rejoin
execute store result score #on lob if entity @a
execute unless entity @a[tag=player] if score #on lob matches 1 as @a[limit=1] run function rlk:lobby/claim
# 더미: 받은 피해를 모으고 체력을 다시 채움 · 밀려나지 않게
execute if score #lobCd lob matches 1.. run scoreboard players remove #lobCd lob 1
scoreboard players set #dd lob 0
execute as @e[tag=rlk_dummy] run function rlk:lobby/dummy
execute as @e[tag=rlk_tutT] run function rlk:lobby/hbfix
# 로비 방 안의 플레이어
execute as @a[tag=player,scores={lobRoom=1..}] run function rlk:lobby/ptick
