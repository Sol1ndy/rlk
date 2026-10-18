# BURST: a star of white/cyan/mint crystal shards and two thin lime crescents (the wing outline).
function rlk:mboss/butterfly/rig_stub/prop/clear
particle minecraft:block{block_state:"minecraft:white_stained_glass"} ~ ~2.2 ~ 1.2 1.5 1.2 0 36 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:light_blue_stained_glass"} ~ ~2.2 ~ 1 1.3 1 0 22 force @a[tag=player]
particle minecraft:dust{color:[0.729f,0.953f,0.89f],scale:1.6} ~ ~2.2 ~ 1.6 1.6 1.6 0 30 force @a[tag=player]
particle minecraft:dust{color:[0.224f,0.706f,0.757f],scale:1.2} ~ ~2.2 ~ 1.2 1.2 1.2 0 16 force @a[tag=player]
particle minecraft:end_rod ~ ~2.2 ~ 0.2 0.2 0.2 0.22 24 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^-1.55 ^0.67 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^-1.65 ^0.99 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^-1.73 ^1.4 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^-1.78 ^1.88 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^-1.8 ^2.4 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^-1.78 ^2.92 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^-1.73 ^3.4 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^-1.65 ^3.81 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^-1.55 ^4.13 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^1.55 ^0.67 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^1.65 ^0.99 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^1.73 ^1.4 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^1.78 ^1.88 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^1.8 ^2.4 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^1.78 ^2.92 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^1.73 ^3.4 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^1.65 ^3.81 ^ 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.784f,0.941f,0.376f],scale:1} ^1.55 ^4.13 ^ 0 0 0 0 1 force @a[tag=player]
execute positioned ^ ^2.2 ^ rotated ~ ~ run function rlk:mboss/butterfly/tc/card {kind:"burst",bb:"center",roll:0,spin:25,s0:1,s1:6.5,move:"0f,0f,0f",life:7,fade:3,col:16383484,ax:"0f,0f,1f"}
execute positioned ^ ^2.2 ^ rotated ~ ~ run function rlk:mboss/butterfly/tc/card {kind:"glow",bb:"center",roll:0,spin:0,s0:2,s1:5,move:"0f,0f,0f",life:6,fade:3,col:12252131,ax:"0f,0f,1f"}
execute positioned ^ ^2.2 ^ rotated ~0 -50 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:10,fade:5,col:12252131,ax:"0f,0f,1f"}
execute positioned ^ ^2.2 ^ rotated ~45 -25 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:10,fade:5,col:7919825,ax:"0f,0f,1f"}
execute positioned ^ ^2.2 ^ rotated ~90 0 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:10,fade:5,col:16383484,ax:"0f,0f,1f"}
execute positioned ^ ^2.2 ^ rotated ~135 25 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:10,fade:5,col:3781825,ax:"0f,0f,1f"}
execute positioned ^ ^2.2 ^ rotated ~180 -50 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:10,fade:5,col:12252131,ax:"0f,0f,1f"}
execute positioned ^ ^2.2 ^ rotated ~225 -25 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:10,fade:5,col:7919825,ax:"0f,0f,1f"}
execute positioned ^ ^2.2 ^ rotated ~270 0 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:10,fade:5,col:16383484,ax:"0f,0f,1f"}
execute positioned ^ ^2.2 ^ rotated ~315 25 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.6,s1:1.6,move:"0f,0f,0f",life:10,fade:5,col:3781825,ax:"0f,0f,1f"}
execute rotated as @s rotated ~ 0 run execute positioned ^-1.5 ^2.6 ^ rotated ~ ~ run function rlk:mboss/butterfly/tc/card {kind:"moon",bb:"fixed",roll:0,spin:0,s0:2,s1:3.2,move:"0f,0f,0f",life:8,fade:4,col:13168736,ax:"0f,0f,1f"}
execute rotated as @s rotated ~ 0 run execute positioned ^1.5 ^2.6 ^ rotated ~ ~ run function rlk:mboss/butterfly/tc/card {kind:"moon",bb:"fixed",roll:180,spin:0,s0:2,s1:3.2,move:"0f,0f,0f",life:8,fade:4,col:13168736,ax:"0f,0f,1f"}
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 1 1 0.33
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.8 1.3 0.27
playsound minecraft:entity.breeze.wind_burst hostile @a[tag=player] ~ ~ ~ 0.8 1.2 0.27
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.9 1.6 0.3
