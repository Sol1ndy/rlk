# B2 pattern tick 76
function rlk:boss/arlecchino/rig_stub/look/glow/crimson
function rlk:boss/arlecchino/rig_stub/anchor/palm_r
execute at @s run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
execute at @e[tag=rlk_kn_anchor,limit=1] run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.2 0.2 0.2 0 10 force @a[tag=player]
