# 스킬 피해를 준 뒤 (@s = 플레이어, at @s): 처치 효과
# 원소폭발 피해 표시를 내림(균형치: 다음 공격이 원소폭발로 세지지 않게)
scoreboard players set #burstDmg tmp 0
execute if score #mobKilled tmp matches 1.. run function rlk:combat/on_kill
