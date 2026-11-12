# 퍼펙트 닷지의 박자를 시작한다 (@s = 플레이어; player/def/fx/pd = pd_go, 닷지 한 번에 한 번; 태그 rlk_hc_atk = 공격한 적).
# round W(사용자: 「퍼펙트 닷지의 모션이 너무 느려」): 느린 준비 자세를 없애고 그 틱에 바로 뒤로 넘는다. 시간표(실제 틱, 0 = 맞았을 틱):
# 0 붉은 분홍 터짐 · 잔상 · 어두운 테두리 · 낮은 붐 · **도약**(클립 pdodge 시작) → 1~8 느린 화면 ×1/2(세계는 2 · 4 · 6 · 8틱에만 돎: 세계 틱 넷) 동안
# 아바타는 제 속도로 백 핸드스프링(1~6 한 틱에 60도씩 뒤로 한 바퀴, 3 = 정점에서 거꾸로 서 다리를 벌림) → 7 착지(적을 보고, 붉은 기운이 걷힘)
# → 8 착지를 받아 낮춤 · 느린 화면 끝 → 10 준비 자세 → 14 끝. 예전(round V): 5틱 뒤에야 클립을 시작해 9틱 동안 ×1/3 로 두 팔을 든 채 버틴 뒤
# 14~21 에 넘고 26 에 준비 자세였다.
# 세계가 멈춘 틱 = 1 · 3 · 5 · 7(4틱; 예전 7틱). 1~11틱 동안 플레이어는 맞지 않는다(그 사이의 세계 틱 2 · 4 · 6 · 8 · 9 · 10 · 11 = 일곱: 예전과
# 같은 수). #btOn tmp 0 이면 세계를 멈추지 않고 효과만
execute if score #btK cb matches 1.. run function rlk:player/def/beat/end
scoreboard players set #btK cb 2
scoreboard players set #btA cb 0
scoreboard players set #btAct cb 0
tag @e[tag=rlk_hc_atk,limit=1] add rlk_bt_atk
function rlk:player/def/fx/ovl {g:"vig",in:1,hold:7,out:3,t:11}
execute if entity @e[tag=rlk_dgo,limit=1] at @e[tag=rlk_dgo,limit=1] run function rlk:player/def/fx/pd_at
execute unless entity @e[tag=rlk_dgo,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:player/def/fx/pd_at
execute at @e[tag=rlk_body,limit=1] run function rlk:player/def/fx/pd_body
# 아바타: 그 틱에 바로 뒤로 넘는 동작(리그 캐릭터의 클립 · 마네킹 캐릭터의 대역 리그)과 붉은 분홍 기운
function rlk:char/motion/beat/dodge
