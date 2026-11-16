# entrance tick 90
function rlk:mboss/butterfly/fx/p/land
function rlk:mboss/butterfly/fx/snd/land
playsound minecraft:block.moss.fall hostile @a[tag=player] ~ ~ ~ 0.9 1 0.3
particle minecraft:poof ~ ~0.15 ~ 0.6 0.05 0.6 0.03 10 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.7 0.05 0.7 0 14 force @a[tag=player]
function rlk:mboss/butterfly/fx/card {kind:"ripple",pos:"~ ~0.06 ~",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:1,s1:3,move:"0f,0f,0f",life:5,fade:2,col:11985754}
