execute if score @s pmActive matches 1 run function rlk:char/motion/finish
# 실제 대쉬 (@s = 플레이어, at @s): 무적 + 효과 + 방향/이동
# 무적 6틱(0.3초). 대쉬는 동작으로 보이게 하고(char/motion/dash) 입자는 발밑에 조금만
scoreboard players set @s dashInvT 6
# 진행 중인 평타는 취소(아직 안 들어간 타격 포함)하고, 다음 평타는 1타부터
scoreboard players set @s comboStep 0
scoreboard players set @s pmAtkPending 0
scoreboard players set @s naQ 0
scoreboard players set @s naQn 0
scoreboard players set @s atkCD 0
execute unless score #k206 snd matches 1 run function rlk:snd/f226
execute unless score #k207 snd matches 1 run function rlk:snd/f227
execute at @e[tag=rlk_body,limit=1] run particle minecraft:cloud ~ ~0.15 ~ 0.2 0.03 0.2 0.01 3
# 현재 이동 입력 방향(없으면 시선 방향)으로 이동 시작
function rlk:player/dash_dir
# 캐릭터 대쉬 동작(있는 캐릭터만)
function rlk:char/motion/dash
# 아이템 대쉬 트리거
function rlk:items/hook/on_dash
