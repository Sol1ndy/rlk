# @s = zone marker, at @s (the 중간보스 zone centre, where the gate stood); the player is back in the dungeon.
# No selection screen and no fanfare here: cur.picks item boxes fall onto the floor (mboss/box/*). Each box is
# a room object (oact 15, room/obj/k_mbox); one click = one chapter-rarity, items-only pick (room/obj/do_mbox).
title @a[tag=player] times 8 50 14
title @a[tag=player] subtitle [{text:"아이템 상자 ",color:"#FFE08A"},{nbt:"cur.picks",storage:"rlk:mboss",color:"#FFE08A"},{text:"개 · 챕터 등급",color:"#FFE08A"}]
title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" 처치",color:"#FFE08A",bold:true}]
scoreboard players set @a[tag=player] vBig 72
scoreboard players set @a[tag=player] ttlT 72
execute store result score #mbPk mb run data get storage rlk:mboss cur.picks
execute if score #mbPk mb matches 1.. run function rlk:mboss/box/drop_all
