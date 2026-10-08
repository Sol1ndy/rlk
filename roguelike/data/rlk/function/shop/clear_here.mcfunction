# @s = 구매 버튼, at @s. 구매된 슬롯(같은 shopGid)의 아이템/이름/버튼 제거(블록은 유지, 리롤 시 다시 채워짐)
particle minecraft:cloud ~ ~ ~ 0.3 0.3 0.3 0.02 15
playsound minecraft:entity.item.pickup master @a ~ ~ ~ 0.5 1.2
scoreboard players operation #sg tmp = @s shopGid
execute as @e[tag=rlk_shop_item,distance=..4] if score @s shopGid = #sg tmp run kill @s
execute as @e[tag=rlk_shop_info,distance=..4] if score @s shopGid = #sg tmp run kill @s
execute as @e[tag=rlk_shop_lbl,distance=..4] if score @s shopGid = #sg tmp run kill @s
kill @s
