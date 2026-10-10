# 로비 더미 · 허수아비의 레벨 · 체력 숫자가 벽 너머로 보이지 않게(한 번만) (@s = 몹)
execute if entity @s[tag=rlk_dsee] run return 0
scoreboard players set #t lob 0
execute store success score #t lob on passengers if entity @s[tag=!rlk_hb_bg,tag=!rlk_hb_fg] run data merge entity @s {see_through:0b}
execute if score #t lob matches 1 run tag @s add rlk_dsee
