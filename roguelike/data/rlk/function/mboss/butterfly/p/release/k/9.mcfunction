# release clock 9
function rlk:mboss/butterfly/rig_stub/face/track
execute rotated as @s rotated ~ 0 positioned ~ ~0.06 ~ run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~90 90",bb:"fixed",roll:0,spin:0,s0:2,s1:3,move:"0f,0f,0f",life:4,fade:2,col:11985754}
particle minecraft:cherry_leaves ~ ~0.6 ~ 0.6 0.2 0.6 0 2 force @a[tag=player]
playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.5 1.3 0.17
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.8} ~ ~ ~ 0.3 0.3 0.3 0 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.8} ~ ~ ~ 0.3 0.3 0.3 0 3 force @a[tag=player]
