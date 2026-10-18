# @s = the blade (#pjEv 1 wall, 2 life over, 4 hit the player). A hit: a spark at the player, the blade flies on
# harmlessly (#pjKeep 1, the framework default). The wall or the end of its life: it shatters.
execute if score #pjEv mb matches 4 run return run function rlk:mboss/butterfly/p/vacuum/hit
function rlk:mboss/butterfly/fx/card {kind:"burst",pos:"~ ~1.1 ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:3,move:"0f,0f,0f",life:4,fade:2,col:16777215}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"shard",pos:"~ ~1.1 ~",rot:"~-4.2 75.9",bb:"fixed",roll:-3,spin:0,s0:0.5,s1:1.2,move:"0f,1.8f,0f",life:8,fade:4,col:11135357}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"shard",pos:"~ ~1.1 ~",rot:"~71.7 76.4",bb:"fixed",roll:-15,spin:0,s0:0.5,s1:1.2,move:"0f,1.8f,0f",life:8,fade:4,col:11135357}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"shard",pos:"~ ~1.1 ~",rot:"~142.4 43.3",bb:"fixed",roll:10,spin:0,s0:0.5,s1:1.2,move:"0f,1.8f,0f",life:8,fade:4,col:11135357}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"shard",pos:"~ ~1.1 ~",rot:"~223.8 77.6",bb:"fixed",roll:1,spin:0,s0:0.5,s1:1.2,move:"0f,1.8f,0f",life:8,fade:4,col:11135357}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"shard",pos:"~ ~1.1 ~",rot:"~288.6 68.9",bb:"fixed",roll:-10,spin:0,s0:0.5,s1:1.2,move:"0f,1.8f,0f",life:8,fade:4,col:11135357}
particle minecraft:block{block_state:"minecraft:lime_stained_glass"} ~ ~1.0 ~ 0.8 1.2 0.3 0 14 force @a[tag=player]
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
playsound minecraft:entity.breeze.wind_burst hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
scoreboard players set #pjKeep mb 0
