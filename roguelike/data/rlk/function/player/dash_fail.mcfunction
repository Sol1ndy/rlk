# 닷지 재사용 대기 중 (@s = 플레이어): 짧은 둔탁한 소리(누르고 있어 4틱마다 반복되는 우클릭은 소리 없이)
execute if score @s rcT matches 2.. run return 0
execute unless score #k198 snd matches 1 run function rlk:snd/f228
