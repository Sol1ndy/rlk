# @s = zone marker; the player is back in the dungeon and #combat is 0, so lvup/toggle opens and
# saves this spot as its return point. pkMb keeps character cards out of these picks (lvup/roll).
title @a[tag=player] times 8 50 14
title @a[tag=player] subtitle [{text:"아이템 선택 ",color:"#FFE08A"},{nbt:"cur.picks",storage:"rlk:mboss",color:"#FFE08A"},{text:"번 (챕터 등급)",color:"#FFE08A"}]
title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" 처치",color:"#FFE08A",bold:true}]
scoreboard players set @a[tag=player] vBig 72
scoreboard players set @a[tag=player] ttlT 72
execute as @a[tag=player] at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.8 1
execute as @a[tag=player,limit=1] run function rlk:lvup/add with storage rlk:mboss cur.rw
execute store result score #mbPk mb run data get storage rlk:mboss cur.picks
execute as @a[tag=player,limit=1] run scoreboard players operation @s pkMb += #mbPk mb
execute as @a[tag=player,limit=1] at @s unless score @s pkMode matches 1.. run function rlk:lvup/toggle
