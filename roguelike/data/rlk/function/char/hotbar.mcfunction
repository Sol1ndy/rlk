# 스킬(1번)·폭발(2번) 칸 유지 (@s = 플레이어). 표시가 바뀔 때만 다시 만든다
# 스킬 칸: 키 = 남은 재사용 대기(초, 올림). 0 = 사용 가능
scoreboard players operation #sk tmp = @s skillCd
scoreboard players add #sk tmp 19
scoreboard players operation #sk tmp /= #st20 tmp
# 클로린드: 밤 순찰 중에는 재사용 대기 대신 빛나는 스킬 아이템(-1)
execute if score #charN tmp matches 4 if score @s clNV matches 1.. run scoreboard players set #sk tmp -1
# 나비아: 충전이 남아 있으면 키 = -10 - 충전 수(개수로 보여 줌)
execute if score #charN tmp matches 6 if score @s nvC matches 1.. run scoreboard players operation #sk tmp = @s nvC
execute if score #charN tmp matches 6 if score @s nvC matches 1.. run scoreboard players operation #sk tmp *= #neg1 tmp
execute if score #charN tmp matches 6 if score @s nvC matches 1.. run scoreboard players remove #sk tmp 10
execute if score #charN tmp matches 8 if score @s nfC matches 1.. run scoreboard players operation #sk tmp = @s nfC
execute if score #charN tmp matches 8 if score @s nfC matches 1.. run scoreboard players operation #sk tmp *= #neg1 tmp
execute if score #charN tmp matches 8 if score @s nfC matches 1.. run scoreboard players remove #sk tmp 10
# 로노바: 사형 선고를 쓸 수 있고 잔향이 있으면 키 = -10 - 잔향 수
execute if score #charN tmp matches 7 if score @s skillCd matches ..0 if score @s rnEn matches 1.. run scoreboard players operation #sk tmp = @s rnEn
execute if score #charN tmp matches 7 if score @s skillCd matches ..0 if score @s rnEn matches 1.. run scoreboard players operation #sk tmp *= #neg1 tmp
execute if score #charN tmp matches 7 if score @s skillCd matches ..0 if score @s rnEn matches 1.. run scoreboard players remove #sk tmp 10
scoreboard players set #mk tmp 0
execute unless score #sk tmp = @s skShown run scoreboard players set #mk tmp 1
# 칸에 실제로 있는 개수(없으면 0)가 기대값(대기 중 = 남은 초, 아니면 1. 최대 64)과 다르면 다시 만든다 — 버리기 키로 개수가 줄어든 경우 포함
scoreboard players operation #want tmp = #sk tmp
execute if score #want tmp matches ..0 run scoreboard players set #want tmp 1
execute if score #want tmp matches 65.. run scoreboard players set #want tmp 64
execute if score #sk tmp matches ..-11 run scoreboard players set #want tmp -10
execute if score #sk tmp matches ..-11 run scoreboard players operation #want tmp -= #sk tmp
execute store result score #have tmp if items entity @s hotbar.1 *[minecraft:custom_data~{rlk_ui:{role:"skill"}}]
execute unless score #have tmp = #want tmp run scoreboard players set #mk tmp 1
execute if score #mk tmp matches 1 run function rlk:char/skill_item
# 폭발 칸: 키 = 원소 에너지(pt) × 100 + 남은 재사용 대기(초)
scoreboard players operation #bs tmp = @s burstCd
scoreboard players add #bs tmp 19
scoreboard players operation #bs tmp /= #st20 tmp
scoreboard players operation #bk tmp = @s energyPt
scoreboard players operation #bk tmp *= #100 tmp
scoreboard players operation #bk tmp += #bs tmp
scoreboard players set #mk tmp 0
execute unless score #bk tmp = @s buShown run scoreboard players set #mk tmp 1
scoreboard players operation #want tmp = #bs tmp
execute if score #want tmp matches ..0 run scoreboard players set #want tmp 1
execute if score #want tmp matches 65.. run scoreboard players set #want tmp 64
execute store result score #have tmp if items entity @s hotbar.2 *[minecraft:custom_data~{rlk_ui:{role:"burst"}}]
execute unless score #have tmp = #want tmp run scoreboard players set #mk tmp 1
execute if score #mk tmp matches 1 run function rlk:char/burst_item
