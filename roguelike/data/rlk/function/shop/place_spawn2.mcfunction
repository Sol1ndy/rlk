# at = 블록 코너. gid 발급 + 기록 저장 + 가격 + 엔티티 스폰
scoreboard players add #shopcnt shopGid 1
scoreboard players operation #sgid tmp = #shopcnt shopGid
execute store result storage rlk:shop key int 1 run scoreboard players get #sgid tmp
function rlk:shop/store_rec with storage rlk:shop
# 상점 노드의 기록은 맵이 바뀔 때 지운다(room/clear → shop/node/forget)
execute if score #shopNode tmp matches 1 run data modify storage rlk:shop nodekeys append from storage rlk:shop key
data modify storage rlk:io rr set from storage rlk:io rarity
function rlk:shop/get_price with storage rlk:io
function rlk:shop/spawn_ent with storage rlk:io
execute as @e[tag=rlk_shop_new] run scoreboard players operation @s shopGid = #sgid tmp
data modify entity @e[tag=rlk_shop_info,tag=rlk_shop_new,limit=1] text set from storage rlk:io name
# 레전더리/신화: 드롭과 동일한 오라
execute if data storage rlk:io {rarity:"legendary"} run tag @e[tag=rlk_shop_item,tag=rlk_shop_new] add rlk_shop_aura
execute if data storage rlk:io {rarity:"mythic"} run tag @e[tag=rlk_shop_item,tag=rlk_shop_new] add rlk_shop_aura
# 상점 노드의 진열대는 맵이 바뀌면 함께 사라진다(room/clear)
execute if score #shopNode tmp matches 1 run tag @e[tag=rlk_shop_new] add rlk_room
tag @e[tag=rlk_shop_new] remove rlk_shop_new
