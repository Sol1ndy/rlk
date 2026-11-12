# From room/combat_clear on a rlk_riftz zone (@s = the zone marker, at it; the room's own fight is over): its dormant
# rift grows open (state 5 for 20 t, then 2).
scoreboard players operation #riftZid room = @s zid
execute as @e[type=minecraft:marker,tag=rlk_rift,scores={riftS=1}] if score @s zid = #riftZid room at @s run function rlk:room/rift/grow
