# 평타 휘두르기 느려짐 (@s = 플레이어). rlk:tick 이 매 틱 view/tick 보다 먼저 부른다: view/move(숄더뷰 · F5 시점)와 1인칭 속성
# 수정자가 이 틱의 같은 값을 쓴다.
# swHold 1 = 휘두르는 중: 평타를 시작한 순간부터 다음 평타 입력을 받는 틱(player/tick 의 #pmChainOpen 1) 전까지. 그동안 걷기는 절반
#   속도(숄더뷰 · F5, #swSlow)이고 점프는 막힌다. 1인칭은 점프만 막는다(아래).
#   평타 간격 atkCD 가 남아 있으면 휘두르는 중이다. atkCD 는 평타만 정한다: 근접 combat/combo_after1·2(루미네 · 클로린드 · 네페르),
#   활 char/bow/na · bow/release, 클로린드 권총 char/clorinde/shoot, 로노바 char/ronova/na, 네페르 환영극, 리그 캐릭터(스커크 ·
#   아를레키노 · 나비아) char/motion/combat/request. 대쉬(player/dash_go)는 atkCD 를 0으로 만들어 바로 풀린다.
#   리그 캐릭터는 그 평타 동작이 재생 중일 때만(char/motion/combat/swing_clip): 동작이 끝나거나 멈추거나(사망 · 지도 · 선택 화면 ·
#   캐릭터 변경 · 시점 전환) 다른 동작(대쉬 · 스킬 · 폭발 · 집어넣기)으로 바뀌면 풀린다.
# 이벤트에 기대지 않고 매 틱 다시 구하므로, 놓친 이벤트나 사라진(또는 남은) 수정자가 있어도 다음 틱에 맞춰진다.
scoreboard players set #swHold tmp 0
execute if score @s atkCD matches 1.. run scoreboard players set #swHold tmp 1
execute if score #swHold tmp matches 1 unless function rlk:char/motion/combat/swing_clip run scoreboard players set #swHold tmp 0
# 스킬 · 원소폭발로 끊긴 휘두르기(player/swing/cut, swCut = 그때 남은 atkCD): 그 간격이 끝날 때까지 잡지 않는다. 그 뒤에 시작한
# 새 평타는 atkCD 가 swCut 보다 커지므로 다시 잡는다. swCut 은 atkCD 를 따라 줄어 간격이 끝나면 0이 된다.
execute if score @s swCut matches 1.. if score @s atkCD > @s swCut run scoreboard players set @s swCut 0
execute if score @s swCut matches 1.. run scoreboard players set #swHold tmp 0
execute if score @s swCut matches 1.. run scoreboard players operation @s swCut = @s atkCD
# 쉬는 상태(사망 · 지도 화면 · 선택 공간 · 보스 연출 카메라)에서는 풀린다
execute if score @s dead matches 1 run scoreboard players set #swHold tmp 0
execute if score @s vMap matches 1 run scoreboard players set #swHold tmp 0
execute if score @s pkMode matches 1.. run scoreboard players set #swHold tmp 0
execute if score @s rdCam matches 1 run scoreboard players set #swHold tmp 0
# 숄더뷰 · F5 시점: view/move 가 이 값을 보고 아바타를 절반 속도로 걷게 하고(달리기 배율 없음) 점프를 하지 않는다.
scoreboard players operation @s swHold = #swHold tmp
# 1인칭(몸 = 플레이어): 점프 힘 ×0 (수정자 rlk:swing_hold)만 붙이고, 걷기는 제 속도 그대로다. 이동 속도 속성은 건드리지 않는다:
# 바닐라 클라이언트는 시야(FOV)를 (이동 속도 ÷ 걷기 속도 + 1) ÷ 2 배로 바꾸므로, 이동 속도를 낮추면 휘두를 때마다 화면이 확대된다.
# 시야를 바꾸지 않고 1인칭 걷기를 늦출 바닐라 방법(투명한 탈것에 태우기 등)은 휘두를 때마다 화면이 튀어서 쓰지 않았다(README 3절).
# 매 틱 다시 붙이거나 뗀다: 이미 있는 수정자의 add 와 없는 수정자의 remove 는 아무것도 바꾸지 않으므로, 사라진 수정자는 다시
# 붙고 남은 수정자는 떨어진다.
scoreboard players set #swMod tmp 0
execute if score @s swHold matches 1 if entity @s[tag=rlk_body] run scoreboard players set #swMod tmp 1
execute if score #swMod tmp matches 1 run attribute @s minecraft:jump_strength modifier add rlk:swing_hold -1 add_multiplied_total
execute if score #swMod tmp matches 0 run attribute @s minecraft:jump_strength modifier remove rlk:swing_hold
# D12 판(휘두르는 동안 정지)이 저장해 둔 이동 속도 수정자 rlk:swing_hold 를 한 번만 지운다(그 판에서 휘두르는 중에 저장하고
# 나갔으면 남아 있어 걷지 못함). 지운 플레이어에게는 태그 rlk_sw13 을 붙여 다시 하지 않는다.
execute unless entity @s[tag=rlk_sw13] run function rlk:player/swing/legacy
# 1인칭 점프(통계 swJump): 평타 사이 간격에서 뛰면 다음 평타는 1타부터. 휘두르는 동안 들어온 점프(수정자가 클라이언트에 닿기 전
# 지연으로 뛴 경우)는 무시한다. 클릭보다 먼저 들어온 점프는 combat/on_attack 이 클릭 전에 처리한다. 숄더뷰 점프는 view/move.
execute if score @s swJump matches 1.. if score @s swHold matches 0 if entity @s[tag=rlk_body] run function rlk:player/swing/jump
scoreboard players set @s swJump 0
