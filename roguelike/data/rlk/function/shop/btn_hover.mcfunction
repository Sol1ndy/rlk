# @s = 상점 버튼(구매/리롤), at @s. 호버 진입/이탈
execute if entity @s[tag=rlk_shop_hover] unless entity @s[tag=rlk_shop_hov_on] run function rlk:shop/hover_enter
execute unless entity @s[tag=rlk_shop_hover] if entity @s[tag=rlk_shop_hov_on] run function rlk:shop/hover_exit
