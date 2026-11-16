# 닷지 재사용 대기 중 (@s = 플레이어): 짧은 둔탁한 소리. 누르고 있어 4틱마다 반복되는 우클릭(눈앞 실드의 반복 클릭 · F5 의 아이템 사용
# combat/rc_hold 모두: 바로 앞 시도가 5틱 안, #dgTryD cb ← player/dash)은 소리 없이
execute if score #dgTryD cb matches ..5 run return 0
execute unless score #k198 snd matches 1 run function rlk:snd/f228
