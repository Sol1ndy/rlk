# @s = 플레이어, at @s. 받은 F(패링 입력): 지금 틱을 찍고 다음 입력까지 #parGap 틱. 진행 중인 평타는 끊고(대쉬와 같게) 가드 자세
scoreboard players operation @s parAt = #now cb
scoreboard players operation @s parLk = #now cb
scoreboard players operation @s parLk += #parGap tmp
execute if score @s pmActive matches 1 run function rlk:char/motion/finish
scoreboard players set @s comboStep 0
scoreboard players set @s pmAtkPending 0
scoreboard players set @s naQ 0
scoreboard players set @s naQn 0
scoreboard players set @s atkCD 0
function rlk:player/def/guard
# 아이템 · 튜토리얼 신호
function rlk:items/hook/on_parry_press
