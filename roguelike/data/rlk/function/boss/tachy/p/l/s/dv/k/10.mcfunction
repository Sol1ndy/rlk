# L stage dv tick 10
function rlk:boss/tachy/rig/play/l_shock
execute at @e[type=minecraft:marker,tag=rlk_tk_llock,limit=1] run function rlk:boss/tachy/fx/p/impact {el:3}
execute at @e[type=minecraft:marker,tag=rlk_tk_llock,limit=1] positioned ~ ~0.1 ~ run function rlk:boss/tachy/fx/p/dust_ring {r:20}
function rlk:boss/tachy/fx/snd/chop
