# 상점이 존재할 때만 실행. 레이캐스트는 상점 근처(10블록) 플레이어에 한해 1회만
scoreboard players set #shopAimGid tmp 0
tag @e[tag=rlk_shop_btn] remove rlk_shop_hover
tag @e[tag=rlk_shop_reroll] remove rlk_shop_hover
execute as @a[tag=player] at @s if entity @e[tag=rlk_shop_btn,distance=..14] anchored eyes run function rlk:shop/aim
execute as @a[tag=player] at @s unless entity @e[tag=rlk_shop_btn,distance=..14] if entity @e[tag=rlk_shop_reroll,distance=..14] anchored eyes run function rlk:shop/aim
execute as @e[tag=rlk_shop_info] run function rlk:shop/disp
execute as @e[tag=rlk_shop_btn] at @s run function rlk:shop/btn_hover
execute as @e[tag=rlk_shop_reroll] at @s run function rlk:shop/btn_hover
# 레전더리+ 오라(드롭과 동일)
execute if entity @e[tag=rlk_shop_aura,limit=1] as @e[tag=rlk_shop_aura] at @s run function rlk:ditem/aura
