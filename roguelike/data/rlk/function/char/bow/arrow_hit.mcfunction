# 투사체 명중 (@s = 투사체): 로노바의 구체(7) · 잔향(8)은 char/ronova/proj_hit. 다른 종류(옛 저장의 활 화살)는 피해 없이 사라짐
scoreboard players set #jend tmp 1
execute if score @s aKind matches 7..8 run return run function rlk:char/ronova/proj_hit
kill @s
