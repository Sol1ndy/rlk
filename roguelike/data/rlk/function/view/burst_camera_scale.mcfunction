# 저장된 카메라 설정에는 손대지 않는 일시적 배율: 0~5단계, 100~130%.
execute unless score #bcStep view matches 0..5 run scoreboard players set #bcStep view 0
scoreboard players set #bcSix view 6
scoreboard players operation #bcMul view = #bcStep view
scoreboard players operation #bcMul view *= #bcSix view
scoreboard players add #bcMul view 100
