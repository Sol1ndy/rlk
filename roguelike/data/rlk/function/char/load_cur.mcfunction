# 선택된 캐릭터(rlk:chars cur)의 수치를 스코어로 (macro: id)
$data modify storage rlk:chars cur set from storage rlk:chars registry.$(id)
execute store result score #charN tmp run data get storage rlk:chars cur.n
execute store result score #charElem tmp run data get storage rlk:chars cur.elem
# 무기 종류: 1 근접 / 2 활 / 3 법구. 활의 조준 사격 계수(풀차지 전 / 풀차지)
scoreboard players set #wType tmp 1
execute if data storage rlk:chars cur{weaponType:"bow"} run scoreboard players set #wType tmp 2
execute if data storage rlk:chars cur{weaponType:"catalyst"} run scoreboard players set #wType tmp 3
execute store result score #bowAim tmp run data get storage rlk:chars cur.aim
execute store result score #bowFull tmp run data get storage rlk:chars cur.full
execute store result score #na1 tmp run data get storage rlk:chars cur.na1
execute store result score #na2 tmp run data get storage rlk:chars cur.na2
execute store result score #skillCdT tmp run data get storage rlk:chars cur.skill.cd
execute store result score #burstCdT tmp run data get storage rlk:chars cur.burst.cd
execute store result score #burstCost tmp run data get storage rlk:chars cur.burst.cost
execute store result score #burstCost100 tmp run data get storage rlk:chars cur.burst.cost 100
function rlk:char/hud_setup with storage rlk:chars cur.info
# 설명이 바뀌었을 수 있으니 이미 들고 있는 캐릭터 정보(머리)·무기·스킬·폭발 아이템을 지워 다시 만들게 한다(리로드/캐릭터 선택 때)
clear @a *[minecraft:custom_data~{rlk_char:1b}]
clear @a *[minecraft:custom_data~{rlk_ui:{role:"attack"}}]
clear @a *[minecraft:custom_data~{rlk_ui:{role:"skill"}}]
clear @a *[minecraft:custom_data~{rlk_ui:{role:"burst"}}]
