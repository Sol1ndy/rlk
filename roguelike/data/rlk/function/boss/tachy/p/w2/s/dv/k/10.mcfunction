# W2 stage dv tick 10
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:45,yaw:0,pitch:0,roll:15,el:1}
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:45,yaw:0,pitch:0,roll:15,el:3}
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.2 run function rlk:boss/tachy/fx/p/impact {el:1}
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.2 run function rlk:boss/tachy/fx/p/impact {el:3}
function rlk:boss/tachy/fx/snd/chop
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.1 ^2 run function rlk:boss/tachy/fx/p/dust_ring {r:30}
function rlk:boss/tachy/el/edge
