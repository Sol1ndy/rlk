# at = 블록 코너. 좌표(정수) 저장 후 슬롯 배치
summon minecraft:marker ~ ~ ~ {Tags:["rlk_shop_mk"]}
execute store result storage rlk:shop nx int 1 run data get entity @e[tag=rlk_shop_mk,limit=1] Pos[0]
execute store result storage rlk:shop ny int 1 run data get entity @e[tag=rlk_shop_mk,limit=1] Pos[1]
execute store result storage rlk:shop nz int 1 run data get entity @e[tag=rlk_shop_mk,limit=1] Pos[2]
kill @e[tag=rlk_shop_mk]
data modify storage rlk:shop slot set value {}
data modify storage rlk:shop slot.x set from storage rlk:shop nx
data modify storage rlk:shop slot.y set from storage rlk:shop ny
data modify storage rlk:shop slot.z set from storage rlk:shop nz
data modify storage rlk:shop slots append from storage rlk:shop slot
function rlk:shop/spawn_slot
tellraw @a[distance=..0.01] {"text":"[상점] 슬롯 추가됨","color":"green"}
