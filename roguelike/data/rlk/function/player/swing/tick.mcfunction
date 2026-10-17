# 평타 휘두르기 잠금 (@s = 플레이어). rlk:tick 이 매 틱 view/tick 보다 먼저 부른다: view/move(숄더뷰 · F5 시점)와 1인칭 속성
# 수정자가 이 틱의 같은 값을 쓴다.
# swHold 1 = 휘두르는 중: 평타를 시작한 순간부터 다음 평타 입력을 받는 틱(player/tick 의 #pmChainOpen 1) 전까지 이동 · 점프를 막는다.
#   평타 간격 atkCD 가 남아 있으면 휘두르는 중이다. atkCD 는 평타만 정한다: 근접 combat/combo_after1·2(루미네 · 클로린드 · 네페르),
#   활 char/bow/na · bow/release, 클로린드 권총 char/clorinde/shoot, 로노바 char/ronova/na, 네페르 환영극, 리그 캐릭터(스커크 ·
#   아를레키노 · 나비아) char/motion/combat/request. 대쉬(player/dash_go)는 atkCD 를 0으로 만들어 바로 풀린다.
#   리그 캐릭터는 그 평타 동작이 재생 중일 때만(char/motion/combat/swing_clip): 동작이 끝나거나 멈추거나(사망 · 지도 · 선택 화면 ·
#   캐릭터 변경 · 시점 전환) 다른 동작(대쉬 · 스킬 · 폭발 · 집어넣기)으로 바뀌면 풀린다.
# 이벤트에 기대지 않고 매 틱 다시 구하므로, 놓친 이벤트나 사라진(또는 남은) 수정자가 있어도 다음 틱에 맞춰진다.
scoreboard players set #swHold tmp 0
execute if score @s atkCD matches 1.. run scoreboard players set #swHold tmp 1
execute if score #swHold tmp matches 1 unless function rlk:char/motion/combat/swing_clip run scoreboard players set #swHold tmp 0
# 쉬는 상태(사망 · 지도 화면 · 선택 공간 · 보스 연출 카메라)에서는 풀린다
execute if score @s dead matches 1 run scoreboard players set #swHold tmp 0
execute if score @s vMap matches 1 run scoreboard players set #swHold tmp 0
execute if score @s pkMode matches 1.. run scoreboard players set #swHold tmp 0
execute if score @s rdCam matches 1 run scoreboard players set #swHold tmp 0
# 숄더뷰 · F5 시점: 휘두르기 시작한 틱에 아바타가 걷던 가로 속도를 지운다(view/stop_h). 그 뒤로는 view/move 가 걷는 속도를 주지 않으므로
# 아바타는 제자리에 서고, 넉백(바닐라 피격 · player/knockback) · 떨어지기 · 동작의 전진(stepT)만 몸을 움직인다.
execute if score #swHold tmp matches 1 unless score @s swHold matches 1 if entity @e[tag=rlk_av,limit=1] run function rlk:view/stop_h
scoreboard players operation @s swHold = #swHold tmp
# 1인칭(몸 = 플레이어): 이동 속도 · 점프 힘 ×0 (수정자 rlk:swing_hold). 숄더뷰 · F5 시점에서는 view/move 가 아바타를 세운다
# (카메라 노릇을 하는 진짜 플레이어는 받침에 타 있어 수정자가 시야만 좁힌다). 매 틱 다시 붙이거나 뗀다: 이미 있는 수정자의 add 와
# 없는 수정자의 remove 는 아무것도 바꾸지 않으므로, 사라진 수정자는 다시 붙고 남은 수정자는 떨어진다.
# 넉백(바닐라 피격의 속도, player/knockback 의 순간이동) · 대쉬 · 동작의 전진(stepT)과 중력은 그대로 적용된다.
scoreboard players set #swMod tmp 0
execute if score @s swHold matches 1 if entity @s[tag=rlk_body] run scoreboard players set #swMod tmp 1
execute if score #swMod tmp matches 1 run attribute @s minecraft:movement_speed modifier add rlk:swing_hold -1 add_multiplied_total
execute if score #swMod tmp matches 1 run attribute @s minecraft:jump_strength modifier add rlk:swing_hold -1 add_multiplied_total
execute if score #swMod tmp matches 0 run attribute @s minecraft:movement_speed modifier remove rlk:swing_hold
execute if score #swMod tmp matches 0 run attribute @s minecraft:jump_strength modifier remove rlk:swing_hold
# 1인칭 점프(통계 swJump): 평타 사이 간격에서 뛰면 다음 평타는 1타부터. 휘두르는 동안 들어온 점프(수정자가 클라이언트에 닿기 전
# 지연으로 뛴 경우)는 무시한다. 클릭보다 먼저 들어온 점프는 combat/on_attack 이 클릭 전에 처리한다. 숄더뷰 점프는 view/move.
execute if score @s swJump matches 1.. if score @s swHold matches 0 if entity @s[tag=rlk_body] run function rlk:player/swing/jump
scoreboard players set @s swJump 0
