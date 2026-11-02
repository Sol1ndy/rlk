# Q6 toss (@s = body): each orb to its rim spot (r 22 from the axis, bearing k x 45 deg), an arc
# of 10 t; it rests there pulsing until the impact.
execute as @e[type=minecraft:item_display,tag=rlk_kn_q6o0] positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 0 0 positioned ^ ^ ^22 positioned ~ 201.6 ~ run function rlk:mboss/mv/leap {t:10,h:40}
execute as @e[type=minecraft:item_display,tag=rlk_kn_q6o1] positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 45 0 positioned ^ ^ ^22 positioned ~ 201.6 ~ run function rlk:mboss/mv/leap {t:10,h:40}
execute as @e[type=minecraft:item_display,tag=rlk_kn_q6o2] positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 90 0 positioned ^ ^ ^22 positioned ~ 201.6 ~ run function rlk:mboss/mv/leap {t:10,h:40}
execute as @e[type=minecraft:item_display,tag=rlk_kn_q6o3] positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 135 0 positioned ^ ^ ^22 positioned ~ 201.6 ~ run function rlk:mboss/mv/leap {t:10,h:40}
execute as @e[type=minecraft:item_display,tag=rlk_kn_q6o4] positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 180 0 positioned ^ ^ ^22 positioned ~ 201.6 ~ run function rlk:mboss/mv/leap {t:10,h:40}
execute as @e[type=minecraft:item_display,tag=rlk_kn_q6o5] positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 225 0 positioned ^ ^ ^22 positioned ~ 201.6 ~ run function rlk:mboss/mv/leap {t:10,h:40}
execute as @e[type=minecraft:item_display,tag=rlk_kn_q6o6] positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 270 0 positioned ^ ^ ^22 positioned ~ 201.6 ~ run function rlk:mboss/mv/leap {t:10,h:40}
execute as @e[type=minecraft:item_display,tag=rlk_kn_q6o7] positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated 315 0 positioned ^ ^ ^22 positioned ~ 201.6 ~ run function rlk:mboss/mv/leap {t:10,h:40}
execute at @s run playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
