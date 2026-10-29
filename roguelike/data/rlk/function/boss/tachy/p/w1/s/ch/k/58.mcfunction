# W1 stage ch tick 58
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1 positioned ~ 201.9 ~ run function rlk:boss/tachy/p/w1/wave
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:35,yaw:0,pitch:0,roll:0,el:1}
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:35,yaw:0,pitch:0,roll:0,el:3}
execute at @s run function rlk:boss/tachy/fx/snd/wave_release
