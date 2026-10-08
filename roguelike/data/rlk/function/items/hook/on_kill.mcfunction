# 기본공격 처치 시 아이템 효과 (@s = 플레이어, at @s)
# 봉인된 검: 처치 수만큼 카운트, #kirionNeed(load 에서 설정) 도달 시 마검 키리온으로 변신
execute if score @s it_sealed_sword matches 1.. run scoreboard players operation @s kirionKills += #mobKilled tmp
execute if score @s it_sealed_sword matches 1.. if score @s kirionKills >= #kirionNeed tmp run function rlk:items/proc/kirion_transform
# 기병대장의 동전: 처치 시 원소 에너지
execute if score @s it_cavalry_coin matches 1.. run function rlk:items/proc/cavalry
