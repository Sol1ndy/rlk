# H3 달빛 돌진 (clip dash_kick). Lock D at 3: kick r 1.5 1.2 b past D (tell 12) + ring r 3.5
# around D (tell 16, act 3), one group = one 1.3 hit; the dash 10-12, kick 15, ring 19.
function rlk:mboss/butterfly/rig_stub/face/player
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/p/dash_charge
function rlk:mboss/butterfly/fx/snd/dash_charge
particle minecraft:dust{color:[0.78f,0.859f,0.459f],scale:0.6} ~ ~1.0 ~ 0.9 0.9 0.9 0 3 force @a[tag=player]
particle minecraft:end_rod ~ ~1.0 ~ 0.8 0.6 0.8 0.02 1 force @a[tag=player]
