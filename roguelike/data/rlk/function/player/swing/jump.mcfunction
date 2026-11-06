# 평타 사이 간격에서 뛰었다 (@s = 플레이어; 1인칭은 player/swing/tick · combat/on_attack, 숄더뷰 · F5 시점은 view/move).
# 다음 평타는 1타부터: 콤보 단계(comboStep)를 처음으로 되돌린다. 모든 캐릭터의 연타 순서(근접 · 활 · 법구 · 리그 동작 선택)는
# comboStep 만 읽는다. 휘두르는 동안(swHold)에는 점프가 막혀 있어 여기 오지 않는다.
scoreboard players set @s swJump 0
scoreboard players set @s comboStep 0
