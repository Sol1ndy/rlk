# The falling feather here (rotated straight down): a visual pj (dmg 0, no wall stop).
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_mantle","rlk_tk_air","rlk_tk_pj","rlk_tk_new"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_tk_new] run function rlk:boss/tachy/fx/prop/feather
execute as @e[type=minecraft:item_display,tag=rlk_tk_new] run function rlk:boss/tachy/p/mantle/launch
