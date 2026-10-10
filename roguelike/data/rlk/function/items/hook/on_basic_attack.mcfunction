# 기본공격 시(적중 여부 무관) 아이템 효과 (@s = 플레이어, at @s)
# 마검 키리온: 기본공격 시 참격 (아이템 개수만큼)
scoreboard players operation #repN tmp = @s it_sword_kirion
data modify storage rlk:rep fn set value "items/proc/kirion_slash"
execute if score #repN tmp matches 1.. run function rlk:util/rep_call with storage rlk:rep
# 원소 부여 상태의 휘두르기: 주변 풀 씨앗에 불 → 발화, 번개 → 만개
execute if score @s infuse matches 1 run scoreboard players set @e[tag=rlk_core,distance=..3.5] rxQ 13
execute if score @s infuse matches 3 run scoreboard players set @e[tag=rlk_core,distance=..3.5] rxQ 12
# 고통 & 절망: 기본공격 시 공속/이속 스택
execute if score @s it_pain_despair matches 1.. run function rlk:items/proc/pd_gain
# 빗줄기 검집: 원소폭발 뒤 한동안 기본 공격마다 물의 검
execute if score #rainT itv matches 1.. unless score #rainCd itv matches 1.. if entity @e[tag=rlk_mob,distance=..7,limit=1] run function rlk:items/proc/rain_sword
# 선학의 깃: 대쉬 뒤 첫 기본 공격 → 다음 틱에 바람 폭발
execute if score #craneT itv matches 1.. run scoreboard players set #craneQ itv 1
execute if score #craneT itv matches 1.. run scoreboard players set #craneT itv 0
# 튜토리얼 캐릭터 1쪽: 기본 공격 횟수
execute if score #tutS lob matches 21 if score @s lobRoom matches 2 run scoreboard players add #tutC lob 1
