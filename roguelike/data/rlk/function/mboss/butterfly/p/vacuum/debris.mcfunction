# Every 4 t: rock debris and two lime leaves thrown up and forward, the grass rustle.
particle minecraft:block{block_state:"minecraft:mossy_cobblestone"} ^ ^-0.8 ^ 0.6 0.1 0.2 0.15 2 force @a[tag=player]
function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^0.6 ^-0.5 ^",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.4,move:"0f,1.2f,1.5f",life:10,fade:5,col:11135357}
function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^-0.6 ^-0.5 ^",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.4,move:"0f,1.2f,1.5f",life:10,fade:5,col:11135357}
playsound minecraft:block.grass.break hostile @a[tag=player] ~ ~ ~ 0.5 1 0.17
