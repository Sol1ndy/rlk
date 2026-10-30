# @s = the rift's zone marker, at it; the player is back at the rift. The title "<name> 처치" / "레벨 업 · 아이템 상자 N개",
# exactly one level (cur.lvup 1: sp/lvup, the normal level-up with its usual pick), then the rift collapses
# (room/rift/close, 30 t) and cur.picks item boxes fall where it stood (room/rift/close_end -> mboss/box/drop_all,
# chapter rarity, items-only picks). Gold x goldMul and the sapphire came with the kill (miniboss tag on the body).
title @a[tag=player] times 8 50 14
execute if data storage rlk:mboss cur{lvup:1} run title @a[tag=player] subtitle [{text:"레벨 업 · 아이템 상자 ",color:"#FFE08A"},{nbt:"cur.picks",storage:"rlk:mboss",color:"#FFE08A"},{text:"개",color:"#FFE08A"}]
execute unless data storage rlk:mboss cur{lvup:1} run title @a[tag=player] subtitle [{text:"아이템 상자 ",color:"#FFE08A"},{nbt:"cur.picks",storage:"rlk:mboss",color:"#FFE08A"},{text:"개",color:"#FFE08A"}]
title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" 처치",color:"#FFE08A",bold:true}]
scoreboard players set @a[tag=player] vBig 72
scoreboard players set @a[tag=player] ttlT 72
execute if data storage rlk:mboss cur{lvup:1} as @a[tag=player,limit=1] run function rlk:mboss/sp/lvup
execute store result score #spPk mb run data get storage rlk:mboss cur.picks
scoreboard players operation #spZ mb = @s zid
tag @e[tag=rlk_sp_rk] remove rlk_sp_rk
execute as @e[type=minecraft:marker,tag=rlk_rift] if score @s zid = #spZ mb run tag @s add rlk_sp_rk
# no anchor (a lost rift): the boxes fall at the zone centre at once
scoreboard players operation #mbPk mb = #spPk mb
execute unless entity @e[tag=rlk_sp_rk,limit=1] if score #mbPk mb matches 1.. run function rlk:mboss/box/drop_all
execute as @e[type=minecraft:marker,tag=rlk_sp_rk,limit=1] at @s run function rlk:room/rift/close
tag @e[tag=rlk_sp_rk] remove rlk_sp_rk
