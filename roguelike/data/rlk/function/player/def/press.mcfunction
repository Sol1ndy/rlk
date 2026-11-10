# @s = 플레이어, at @s. 받은 F(패링 입력): 지금 틱을 찍고 다음 입력까지 #parGap × (1 + 헛누름 연속) 틱. 진행 중인 평타는 끊고(대쉬와 같게) 가드 자세
# 헛누름 연속(#parWs cb): 바로 앞에 받은 F 가 아무것도 막지 못했고(parHit < parAt) 그 뒤 #parWsT 틱 안이면 +1(최대 #parWsMax),
# 그보다 오래 쉬었으면 0. 패링이 되면 player/def/par_use 가 지운다(#parWsClr 단계 이상)
scoreboard players operation #t cb = #now cb
scoreboard players operation #t cb -= @s parAt
execute if score @s parHit < @s parAt if score #t cb <= #parWsT tmp if score #parWs cb < #parWsMax tmp run scoreboard players add #parWs cb 1
execute if score #t cb > #parWsT tmp run scoreboard players set #parWs cb 0
scoreboard players operation @s parAt = #now cb
scoreboard players operation #t cb = #parWs cb
scoreboard players add #t cb 1
scoreboard players operation #t cb *= #parGap tmp
scoreboard players operation @s parLk = #now cb
scoreboard players operation @s parLk += #t cb
execute if score @s pmActive matches 1 run function rlk:char/motion/finish
scoreboard players set @s comboStep 0
scoreboard players set @s pmAtkPending 0
scoreboard players set @s naQ 0
scoreboard players set @s naQn 0
scoreboard players set @s atkCD 0
function rlk:player/def/guard
# 아이템 · 튜토리얼 신호
function rlk:items/hook/on_parry_press
