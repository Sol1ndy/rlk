execute if entity @e[tag=rlk_shop_btn,distance=..0.7] run tag @e[tag=rlk_shop_btn,distance=..0.7,limit=1,sort=nearest] add rlk_shop_hover
execute if entity @e[tag=rlk_shop_reroll,distance=..0.7] run tag @e[tag=rlk_shop_reroll,distance=..0.7,limit=1,sort=nearest] add rlk_shop_hover
execute if entity @e[tag=rlk_shop_btn,distance=..0.7] run return 0
execute if entity @e[tag=rlk_shop_reroll,distance=..0.7] run return 0
scoreboard players add #sbray tmp 1
execute if score #sbray tmp >= #rShopB view run return 0
execute positioned ^ ^ ^0.35 run function rlk:shop/aim_btn_step
