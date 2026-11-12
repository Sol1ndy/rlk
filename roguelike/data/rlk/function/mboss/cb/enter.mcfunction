# @s = the kind-9 chapter zone marker, at it (from room/zone_enter instead of combat_start): the zone is cleared for
# objects (zst 3) and the gate object stands at its centre (room/obj/k_cboss, oact 16, texts from cprep.<boss_id>.gate).
scoreboard players set @s zst 3
function rlk:room/obj/k_cboss
execute unless score #k10 snd matches 1 run function rlk:snd/f10
