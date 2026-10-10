# @s = 공격한 플레이어, #lcStamp = 실제 클릭의 game time.
# 즉시 발전 과제 + 다음 틱 interaction 폴링으로 같은 클릭이 두 번 실행되는 것을 막는다.
# 새 틱의 클릭은 그대로 받는다. 일반 공격/스킬/지도/UI의 기존 잠금 판단은 on_attack이 맡는다.
execute if score #lcStamp tmp <= @s lcSeen run return 0
scoreboard players operation @s lcSeen = #lcStamp tmp
function rlk:combat/on_attack
