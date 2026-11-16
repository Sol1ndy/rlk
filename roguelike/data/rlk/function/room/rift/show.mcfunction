# From room/zone_enter (after zst 2, before the combat return) and room/zone_first (last) on a rlk_riftz zone (@s =
# the zone marker, at it). A combat room whose fight is still to come (zkind 1, zst <= 2) shows the rift at once,
# dormant; any other zone queues the show for the next rift tick (rlk_riftq), when the zone's own objects exist and
# the player stands where the map put them (the spot keeps its distances to both). Shown once per zone.
scoreboard players operation #riftZid room = @s zid
execute as @e[type=minecraft:marker,tag=rlk_rift] if score @s zid = #riftZid room run return 0
execute if score @s zkind matches 1 if score @s zst matches ..2 run return run function rlk:room/rift/show_now
tag @s add rlk_riftq
scoreboard players set #riftOn room 1
