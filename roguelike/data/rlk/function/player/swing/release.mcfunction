# 휘두르기 잠금 바로 풀기 (@s = 플레이어): 캐릭터 교체(char/player_init), 'player' 태그를 잃을 때(rlk:tick, 2명 이상).
# 평소에는 player/swing/tick 이 매 틱 다시 구한다.
scoreboard players set @s swHold 0
scoreboard players set @s swCut 0
attribute @s minecraft:movement_speed modifier remove rlk:swing_hold
attribute @s minecraft:jump_strength modifier remove rlk:swing_hold
