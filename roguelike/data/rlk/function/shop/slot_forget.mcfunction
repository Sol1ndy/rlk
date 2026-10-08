# at = 슬롯 블록 코너. 저장된 slots에서 이 좌표 항목 제거
summon minecraft:marker ~ ~ ~ {Tags:["rlk_shop_fk"]}
execute store result storage rlk:shop fx int 1 run data get entity @e[tag=rlk_shop_fk,limit=1] Pos[0]
execute store result storage rlk:shop fy int 1 run data get entity @e[tag=rlk_shop_fk,limit=1] Pos[1]
execute store result storage rlk:shop fz int 1 run data get entity @e[tag=rlk_shop_fk,limit=1] Pos[2]
kill @e[tag=rlk_shop_fk]
data modify storage rlk:shop fscan set from storage rlk:shop slots
data modify storage rlk:shop slots set value []
function rlk:shop/filter_loop
