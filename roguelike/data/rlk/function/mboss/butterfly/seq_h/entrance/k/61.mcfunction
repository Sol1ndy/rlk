# entrance tick 61
execute positioned ~ ~2.1 ~ run function rlk:mboss/butterfly/fx/p/cocoon_glow
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"^ ^2.6 ^",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.8,s1:1.6,move:"0f,0f,0f",life:10,fade:2,col:13295176}
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.12
