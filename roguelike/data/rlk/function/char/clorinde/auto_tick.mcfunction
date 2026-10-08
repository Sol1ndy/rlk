# 자동 연사 중 (@s = 플레이어, at 몸): 밤 순찰이 끝났거나 대쉬하면 끄고, 쏠 수 있을 때마다 쏜다
execute unless score @s clNV matches 1.. run return run function rlk:char/clorinde/auto_off
execute if score @s dashMoveT matches 1.. run return run function rlk:char/clorinde/auto_off
execute if score @s atkCD matches 1.. run return 0
execute if score @s buT matches 1.. run return 0
execute if score @s pkMode matches 1.. run return 0
execute if score @s dead matches 1 run return 0
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{}}] run return 0
function rlk:char/clorinde/shoot
