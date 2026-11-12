# 스킬 · 원소폭발이 휘두르기를 끊는다 (@s = 플레이어; combat/on_skill, 클로린드 밤 꿰뚫기). 리그 캐릭터(스커크 · 아를레키노 · 나비아)는
# 스킬 동작이 평타 동작을 바꾸어 이미 풀리므로(char/motion/combat/swing_clip), 동작이 없는 캐릭터도 같게 한다.
# 그때 남은 평타 간격(atkCD)을 swCut 에 적으면 player/swing/tick 이 그 간격이 끝날 때까지 잡지 않는다. 다음 평타 입력은 지금처럼 그 간격 뒤.
execute if score @s atkCD matches 1.. run scoreboard players operation @s swCut = @s atkCD
