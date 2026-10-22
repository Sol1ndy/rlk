# D12 판에서 넘어온 플레이어 (@s = 플레이어, player/swing/tick 에서 rlk_sw13 태그가 없을 때 한 번):
# 그 판은 1인칭에서 휘두르는 동안 이동 속도에 수정자 rlk:swing_hold(×0)를 붙였다. 휘두르는 중에 저장되면 남아 있으므로 지운다.
# 지금 판은 이동 속도를 건드리지 않는다(점프 힘만, player/swing/tick).
attribute @s minecraft:movement_speed modifier remove rlk:swing_hold
tag @s add rlk_sw13
