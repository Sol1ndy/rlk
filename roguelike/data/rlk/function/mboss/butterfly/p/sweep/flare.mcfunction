# A trail segment flares: flame tongues, a flame line puff, embers; crackle.
function rlk:mboss/butterfly/fx/p/flame_trail
function rlk:mboss/butterfly/fx/card {kind:"flame_tongue",pos:"~0.4 ~ ~",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:0.4,s1:1,move:"0f,0f,0f",life:8,fade:3,col:15755824}
function rlk:mboss/butterfly/fx/card {kind:"flame_tongue",pos:"~-0.4 ~ ~0.2",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:0.4,s1:1,move:"0f,0f,0f",life:8,fade:3,col:15755824}
particle minecraft:flame ~ ~0.3 ~ 0.5 0.3 0.5 0.02 8 force @a[tag=player]
playsound minecraft:block.fire.ambient hostile @a[tag=player] ~ ~ ~ 0.5 1.6 0.17
playsound minecraft:entity.generic.burn hostile @a[tag=player] ~ ~ ~ 0.3 1.4 0.1
