# 받는 치유 → 생명의 계약 (@s = 플레이어, #heal tmp)
scoreboard players operation #bolAdd tmp = #heal tmp
scoreboard players set #heal tmp 0
execute if score #bolAdd tmp matches 1.. run function rlk:player/bol/add
