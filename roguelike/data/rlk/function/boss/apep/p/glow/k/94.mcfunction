# glow #apPT 94
function rlk:boss/apep/play/glow_slams
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p3c]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4.22 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p3","rlk_mb_ap_p3c"]}
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4.22 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p3c,limit=1] ~ ~ ~ ~ 0
execute at @s run function rlk:boss/apep/fx/snd/p3_windup
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/apep/fx/p/spiral_wisps
