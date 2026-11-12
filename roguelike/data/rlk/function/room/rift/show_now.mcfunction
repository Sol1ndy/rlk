# @s = the zone marker, at it: the spot (spot/pick: a marker rlk_riftc), then the anchor and its parts, dormant in a
# combat room whose fight is still to come, else open.
tag @s remove rlk_riftq
scoreboard players operation #riftZid room = @s zid
execute as @e[type=minecraft:marker,tag=rlk_rift] if score @s zid = #riftZid room run return 0
scoreboard players set #riftSt room 2
execute if score @s zkind matches 1 if score @s zst matches ..2 run scoreboard players set #riftSt room 1
kill @e[type=minecraft:marker,tag=rlk_riftc]
function rlk:room/rift/spot/pick
execute as @e[type=minecraft:marker,tag=rlk_riftc,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_zone,tag=rlk_riftcz,limit=1] feet run tp @s ~ ~ ~ ~ 0
tag @s remove rlk_riftcz
execute as @e[type=minecraft:marker,tag=rlk_riftc,limit=1] at @s rotated as @s run function rlk:room/rift/build
scoreboard players set #riftOn room 1
