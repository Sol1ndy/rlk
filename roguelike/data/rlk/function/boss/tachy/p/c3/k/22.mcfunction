# C3 pattern tick 22
function rlk:boss/tachy/rig/look/chest/off
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~2 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:40,yaw:0,pitch:0,roll:30,el:1}
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~2 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:40,yaw:0,pitch:0,roll:30,el:3}
function rlk:boss/tachy/fx/snd/slash_light
