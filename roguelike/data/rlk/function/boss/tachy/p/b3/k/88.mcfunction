# B3 pattern tick 88
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:32,yaw:0,pitch:-62,roll:90,el:1}
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2 run function rlk:boss/tachy/fx/p/impact {el:1}
function rlk:boss/tachy/fx/snd/chop
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.1 ^2 run function rlk:boss/tachy/fx/p/dust_ring {r:14}
