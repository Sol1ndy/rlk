# 회복 진열대 (위치 = 블록 코너, macro: id = heal_s 소 / heal_l 대). 값 · 회복량 = rlk:shop heals.<id>
setblock ~ ~ ~ minecraft:polished_andesite
setblock ~ ~1 ~ minecraft:glass
$data modify storage rlk:io id set value "$(id)"
$data modify storage rlk:io hs set from storage rlk:shop heals.$(id)
data modify storage rlk:io item set from storage rlk:io hs.item
data modify storage rlk:io model set from storage rlk:io hs.item
data modify storage rlk:io price set from storage rlk:io hs.price
data modify storage rlk:io rarity set value "heal"
function rlk:shop/node/heal_text with storage rlk:io hs
scoreboard players add #shopcnt shopGid 1
scoreboard players operation #sgid tmp = #shopcnt shopGid
execute store result storage rlk:shop key int 1 run scoreboard players get #sgid tmp
function rlk:shop/store_rec with storage rlk:shop
data modify storage rlk:shop nodekeys append from storage rlk:shop key
function rlk:shop/spawn_ent with storage rlk:io
execute as @e[tag=rlk_shop_new] run scoreboard players operation @s shopGid = #sgid tmp
data modify entity @e[tag=rlk_shop_info,tag=rlk_shop_new,limit=1] text set from storage rlk:io name
tag @e[tag=rlk_shop_new] add rlk_room
tag @e[tag=rlk_shop_new] remove rlk_shop_new
