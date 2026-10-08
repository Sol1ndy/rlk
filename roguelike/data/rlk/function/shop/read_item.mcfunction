# @s = 상점 아이템(item_display). id/가격 읽기
data modify storage rlk:shop buyid set from entity @s item.components."minecraft:custom_data".rlk_shop.id
execute store result score #buyprice tmp run data get entity @s item.components."minecraft:custom_data".rlk_shop.price
scoreboard players set #shopok tmp 1
