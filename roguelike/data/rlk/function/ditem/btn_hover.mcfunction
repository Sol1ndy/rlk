# @s = 버튼, at @s. 호버 진입/이탈
execute if entity @s[tag=rlk_dhover] unless entity @s[tag=rlk_dhov_on] run function rlk:ditem/hover_enter
execute unless entity @s[tag=rlk_dhover] if entity @s[tag=rlk_dhov_on] run function rlk:ditem/hover_exit
