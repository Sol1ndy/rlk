# B2 pattern tick 44
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:60,yaw:0,pitch:-67,roll:90,el:1}
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:60,yaw:0,pitch:-67,roll:90,el:3}
function rlk:boss/tachy/fx/snd/slash_heavy
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.4 run function rlk:boss/tachy/fx/p/impact {el:1}
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.4 run function rlk:boss/tachy/fx/p/impact {el:3}
function rlk:boss/tachy/el/edge
