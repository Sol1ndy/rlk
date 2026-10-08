# 체력 회복 (@s = 플레이어, 입력: #heal tmp). 생명의 계약이 있으면 그것부터 깎는다
function rlk:items/hook/on_heal
execute if score #heal tmp matches ..0 run return 0
execute if score @s bol matches 1.. run function rlk:player/bol/absorb
scoreboard players operation @s curHealth += #heal tmp
execute if score @s curHealth > @s maxHealth run scoreboard players operation @s curHealth = @s maxHealth
