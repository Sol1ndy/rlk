# @s = 플레이어. 플레이어의 다음 행동(받은 F · 닷지 · 평타 · 스킬 / 폭발)이 박자의 아바타 동작을 끊는다: 리그 캐릭터는 새 클립이 스스로
# 끊고, 마네킹 캐릭터의 대역 리그(char/motion/lite)는 여기서 치운다. 무기의 빛 · 붉은 기운은 박자의 시간표대로 남는다
execute if score @s plActive matches 1 run function rlk:char/motion/lite/stop
# 5틱에 시작하는 퍼펙트 닷지의 넘는 동작은 그 사이에 플레이어가 다른 행동을 했으면 하지 않는다(#btAct cb; beat/start_d 가 0 으로)
scoreboard players set #btAct cb 1
