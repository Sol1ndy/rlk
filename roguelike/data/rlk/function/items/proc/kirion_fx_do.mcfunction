# 나선 파티클 2개(반대편). macro: ang(yaw도), hy(높이 블록)
$execute at @e[tag=rlk_body,limit=1] rotated $(ang) 0 positioned ^0 ^$(hy) ^0.8 run particle minecraft:dust{color:[1.0,0.05,0.05],scale:1.3} ~ ~ ~ 0 0 0 0 1
$execute at @e[tag=rlk_body,limit=1] rotated $(ang) 0 positioned ^0 ^$(hy) ^-0.8 run particle minecraft:dust{color:[1.0,0.05,0.05],scale:1.3} ~ ~ ~ 0 0 0 0 1
