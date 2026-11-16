# hands #apPT 36
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2s0,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s0,limit=1] run function rlk:boss/apep/om/stalk/spawn {i:0}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2s1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s1,limit=1] run function rlk:boss/apep/om/stalk/spawn {i:1}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2,limit=1] run function rlk:boss/apep/om/stalk/spawn {i:2}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3,limit=1] run function rlk:boss/apep/om/stalk/spawn {i:3}
function rlk:boss/apep/om/stalk/play {i:0,clip:"leg_rise"}
function rlk:boss/apep/om/stalk/play {i:1,clip:"leg_rise"}
function rlk:boss/apep/om/stalk/play {i:2,clip:"leg_rise"}
function rlk:boss/apep/om/stalk/play {i:3,clip:"leg_rise"}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] run function rlk:boss/apep/fx/snd/p2_stalks
