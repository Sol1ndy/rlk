# @s = 플레이어, at @s. 받은 F(패링 입력): 지금 틱을 찍고 다음 입력까지 #parGap 틱(언제나 같은 값). 진행 중인 평타는 끊고(닷지와 같게)
# 가드 자세. round W(w_brief §6, 사용자 「없애」): 헛누름이 이어질 때 잠금이 12 → 24 → 36 → 48틱으로 길어지던 사다리(리뷰 A-01 (2))는 없앴다 —
# 원작에는 없다. 막으면 player/def/par_use 가 잠금을 #parChain 틱으로 줄인다(어느 단계든)
scoreboard players operation @s parAt = #now cb
scoreboard players operation @s parLk = #now cb
scoreboard players operation @s parLk += #parGap tmp
function rlk:player/def/beat/act
execute if score @s pmActive matches 1 run function rlk:char/motion/finish
scoreboard players set @s comboStep 0
scoreboard players set @s pmAtkPending 0
scoreboard players set @s naQ 0
scoreboard players set @s naQn 0
scoreboard players set @s atkCD 0
function rlk:player/def/guard
# 아이템 · 튜토리얼 신호
function rlk:items/hook/on_parry_press
