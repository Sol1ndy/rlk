# t37: lock A = the floor under the player (lockp, no lead); 6 landing points (the lock + 5 on r 3.4,
# a random turn), each a disc r 2.0 (tell 12, 120 %), quiet (none row: the orbs flare now and
# fly visibly); volleys A and B share one volley group. The landing markers pair with the orbs by apL.
function rlk:boss/apep/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p35a]
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_kept
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_p35a
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p35a] remove rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p35a] remove rlk_mb_lock
scoreboard players set #apq35J mb 0
execute store result score #apq35X mb run random value 0..71
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] store result entity @s Rotation[0] float 1 run scoreboard players get #apq35X mb
function rlk:mboss/grp_new
scoreboard players operation #apq35G mb = #mbGrp mb
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] positioned ^0 ^0 ^0 positioned ~ 201 ~ run function rlk:boss/apep/p/spiral/land_pt {k:1}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] positioned ^0 ^0 ^3.4 positioned ~ 201 ~ run function rlk:boss/apep/p/spiral/land_pt {k:2}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] positioned ^3.234 ^0 ^1.051 positioned ~ 201 ~ run function rlk:boss/apep/p/spiral/land_pt {k:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] positioned ^1.998 ^0 ^-2.751 positioned ~ 201 ~ run function rlk:boss/apep/p/spiral/land_pt {k:4}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] positioned ^-1.998 ^0 ^-2.751 positioned ~ 201 ~ run function rlk:boss/apep/p/spiral/land_pt {k:5}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p35a,limit=1] positioned ^-3.234 ^0 ^1.051 positioned ~ 201 ~ run function rlk:boss/apep/p/spiral/land_pt {k:6}
# the disc hazards of the last three points one tick later (tell 11: the same strike tick; the per-tick budget)
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p35o,scores={apL=1..6}] at @s run function rlk:boss/apep/fx/p/star_flare
execute at @s run function rlk:boss/apep/fx/snd/q5_flare
