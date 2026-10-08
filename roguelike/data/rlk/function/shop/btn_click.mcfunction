# @s = 클릭된 구매 버튼, at @s. 같은 슬롯(shopGid)의 상점 아이템 정보를 읽고 구매 시도
scoreboard players set #shopok tmp 0
scoreboard players operation #sg tmp = @s shopGid
execute as @e[tag=rlk_shop_item,distance=..4] if score @s shopGid = #sg tmp run function rlk:shop/read_item
scoreboard players set #bought tmp 0
execute if score #shopok tmp matches 1 at @s as @a[tag=player,limit=1] run function rlk:shop/try_buy
data remove entity @s attack
execute if score #bought tmp matches 1 run function rlk:shop/clear_here
