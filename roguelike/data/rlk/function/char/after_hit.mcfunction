# 스킬 피해를 준 뒤 (@s = 플레이어, at @s): 처치 효과
execute if score #mobKilled tmp matches 1.. run function rlk:combat/on_kill
