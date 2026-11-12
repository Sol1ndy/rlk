# W2 stage air tick 28
function rlk:mboss/mv/face
execute at @s rotated as @s rotated ~ 0 positioned ^ ^2 ^1 run function rlk:boss/tachy/p/w2/wave
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:26,yaw:0,pitch:0,roll:90,el:1}
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/slash_arc {r:26,yaw:0,pitch:0,roll:90,el:3}
execute at @s run function rlk:boss/tachy/fx/snd/wave_release
