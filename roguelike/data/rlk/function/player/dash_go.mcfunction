execute if score @s pmActive matches 1 run function rlk:char/motion/finish
# 실제 닷지 (@s = 플레이어, at @s = 몸; #dgMv cb 1 = 일반 닷지의 스텝, 2 = 더블 닷지의 두 번째 동작): 시각 도장 + 효과 + 방향/이동.
# 무적 틱은 없다: 맞는 순간 player/def/judge 가 지금 - dgAt 로 판정(퍼펙트 #dgPW 틱 미만 · 일반 몹 #dgLW 틱 미만). 시작한 자리에
# 판정용 표식(rlk_dgo, 퍼펙트 창 동안)
function rlk:player/def/dodge_stamp
# round V: 박자의 아바타 동작(마네킹 캐릭터의 대역 리그)은 다음 행동이 끊는다
function rlk:player/def/beat/act
# 진행 중인 평타는 취소(아직 안 들어간 타격 포함)하고, 다음 평타는 1타부터
scoreboard players set @s comboStep 0
scoreboard players set @s pmAtkPending 0
scoreboard players set @s naQ 0
scoreboard players set @s naQn 0
scoreboard players set @s atkCD 0
execute if score #dgMv cb matches 1 at @e[tag=rlk_body,limit=1] run function rlk:player/dodge/snd_step
execute if score #dgMv cb matches 2 at @e[tag=rlk_body,limit=1] run function rlk:player/dodge/snd_flip
execute at @e[tag=rlk_body,limit=1] run particle minecraft:cloud ~ ~0.15 ~ 0.2 0.03 0.2 0.01 3
# 현재 이동 입력 방향(없으면 시선 방향)으로 이동 시작
function rlk:player/dash_dir
# 캐릭터의 닷지 동작(리그 캐릭터의 클립 dash / dash2, 마네킹 캐릭터의 웅크림 / 대역 리그)
function rlk:char/motion/dash
# 아이템 닷지 트리거(동작마다 한 번: 더블 닷지는 두 번)
function rlk:items/hook/on_dash
