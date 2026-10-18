# B3 날개 휩쓸개 (clip flap_dive: dive 20, slam 26, fan 28-32, glide 33; lock 16;
# trail [34, 36, 38, 40] strike +10 act 8, two groups).
# wings V-up: the Pyro rim glow, the first big flap
function rlk:mboss/butterfly/rig/face/player
execute rotated as @s rotated ~ 0 positioned ^0 ^3.128 ^0.223 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:1.6,move:"0f,0f,0f",life:20,fade:6,col:16439164}
function rlk:mboss/butterfly/fx/snd/flap_big
execute rotated as @s rotated ~ 0 positioned ^2.442 ^6.428 ^-1.424 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.01 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-2.442 ^6.428 ^-1.424 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.01 2 force @a[tag=player]
