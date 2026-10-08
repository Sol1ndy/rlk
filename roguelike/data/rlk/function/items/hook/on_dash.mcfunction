# 대쉬 발동 시 아이템 효과 (@s = 플레이어, at @s)
# 마검 키리온: 대쉬 시작 지점에 지연 참격 (개수만큼)
scoreboard players operation #repN tmp = @s it_sword_kirion
data modify storage rlk:rep fn set value "items/proc/kirion_dash_mark"
execute if score #repN tmp matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:util/rep_call with storage rlk:rep
# 고통 & 절망: 대쉬 시 공속/이속 스택
execute if score @s it_pain_despair matches 1.. run function rlk:items/proc/pd_gain
# 각인 질주 4개: 이번 대쉬에서 이미 맞은 적 표시 초기화
tag @e[tag=rlk_dhit] remove rlk_dhit
# 열혈 저울: 대쉬하면 공격력 증가
execute if score @s it_kinetic_scale matches 1.. run scoreboard players operation #kinT itv = #kinDur tmp
# 선학의 깃: 대쉬 뒤의 첫 기본 공격
execute if score @s it_crane_feather matches 1.. run scoreboard players operation #craneT itv = #craneDur tmp
