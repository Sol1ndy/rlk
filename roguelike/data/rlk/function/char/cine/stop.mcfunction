# Any executor, no position: the actor gone, the avatar visible again (a rig character's displays, the catalyst too). Does
# nothing when there is no actor; the framework's camera release and every exit path of a sequence call it.
function rlk:char/cine/clear
execute as @e[type=minecraft:item_display,tag=rlk_pm,tag=rlk_cine_hid] run data merge entity @s {view_range:1.5f}
execute as @e[type=minecraft:block_display,tag=rlk_cine_hid] run data merge entity @s {view_range:1f}
tag @e[type=!minecraft:mannequin,tag=rlk_cine_hid] remove rlk_cine_hid
execute as @a[tag=player,limit=1] run function rlk:char/cine/show
tag @e[tag=rlk_cine_hid] remove rlk_cine_hid
data remove storage rlk:cine sp
data remove storage rlk:cine face
scoreboard objectives remove cine
