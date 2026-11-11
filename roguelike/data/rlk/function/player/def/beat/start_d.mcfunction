# 퍼펙트 닷지의 박자를 시작한다 (@s = 플레이어; player/def/fx/pd = pd_go, 닷지 한 번에 한 번; 태그 rlk_hc_atk = 공격한 적).
# 시간표(실제 틱, 0 = 맞았을 틱; review/v/ref_pd.md 4): 0 붉은 분홍 터짐 · 잔상 · 어두운 테두리 · 낮은 붐 → 1 멈춤 한 틱 → 2~5 제 속도(닷지의
# 이동이 끝나고 칼이 잔상을 지나감) → 5 몸을 세우고 두 팔을 듦 → 6~14 느린 화면 ×1/3(세계는 8 · 11 · 14틱에만 한 틱씩 돎) →
# 14~21 백 핸드스프링(뒤로 한 바퀴, 정점에서 거꾸로 서 다리를 벌림, 적을 보고 착지) → 22~26 준비 자세 → 27 끝.
# 세계가 멈춘 틱 = 1 · 6 · 7 · 9 · 10 · 12 · 13(7틱). 1~14틱 동안 플레이어는 맞지 않는다. #btOn tmp 0 이면 세계를 멈추지 않고 효과만
execute if score #btK cb matches 1.. run function rlk:player/def/beat/end
scoreboard players set #btK cb 2
scoreboard players set #btA cb 0
scoreboard players set #btAct cb 0
tag @e[tag=rlk_hc_atk,limit=1] add rlk_bt_atk
function rlk:player/def/fx/ovl {g:"vig",in:2,hold:12,out:3,t:17}
execute if entity @e[tag=rlk_dgo,limit=1] at @e[tag=rlk_dgo,limit=1] run function rlk:player/def/fx/pd_at
execute unless entity @e[tag=rlk_dgo,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:player/def/fx/pd_at
execute at @e[tag=rlk_body,limit=1] run function rlk:player/def/fx/pd_body
# 아바타: 붉은 분홍 기운(리그가 보이는 캐릭터는 지금부터, 마네킹 캐릭터는 5틱에 대역 리그가 설 때부터)
function rlk:char/motion/beat/dodge0
