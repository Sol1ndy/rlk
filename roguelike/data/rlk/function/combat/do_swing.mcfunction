# 스윙 진입 (@s = 플레이어, at @s). 틱당 1회만(이중 인식 방지) → 콤보 진행
execute store result score #now tmp run time query gametime
execute if score @s swungAt = #now tmp run return 0
scoreboard players operation @s swungAt = #now tmp
function rlk:combat/combo
