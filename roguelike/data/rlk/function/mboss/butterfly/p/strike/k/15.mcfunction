# strike clock 15
# HIT (the lane + arc strike): the flat wing blade sweeping across (dark teal under bright lime), a burst at L,
# leaves flung out; the wing-strike recipe and a leafy crackle.
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"cres_lime",pos:"^ ^0.8 ^",rot:"~ 0",bb:"fixed",roll:0,spin:-120,s0:7.5,s1:8.2,move:"0f,0f,0f",life:4,fade:2,col:2322810}
execute rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"cres_lime",pos:"^ ^0.85 ^",rot:"~ 0",bb:"fixed",roll:0,spin:-120,s0:7.2,s1:8,move:"0f,0f,0f",life:4,fade:2,col:16777215}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"burst",pos:"~ ~1 ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.8,s1:2.6,move:"0f,0f,0f",life:4,fade:2,col:16777215}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"~ ~1 ~",rot:"~0 70",bb:"fixed",roll:0,spin:0,s0:0.3,s1:0.22,move:"0f,1.5f,0f",life:12,fade:6,col:11394669}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"~ ~1 ~",rot:"~60 70",bb:"fixed",roll:0,spin:0,s0:0.3,s1:0.22,move:"0f,1.5f,0f",life:12,fade:6,col:11394669}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"~ ~1 ~",rot:"~120 70",bb:"fixed",roll:0,spin:0,s0:0.3,s1:0.22,move:"0f,1.5f,0f",life:12,fade:6,col:11394669}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"~ ~1 ~",rot:"~180 70",bb:"fixed",roll:0,spin:0,s0:0.3,s1:0.22,move:"0f,1.5f,0f",life:12,fade:6,col:11394669}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"~ ~1 ~",rot:"~240 70",bb:"fixed",roll:0,spin:0,s0:0.3,s1:0.22,move:"0f,1.5f,0f",life:12,fade:6,col:11394669}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"~ ~1 ~",rot:"~300 70",bb:"fixed",roll:0,spin:0,s0:0.3,s1:0.22,move:"0f,1.5f,0f",life:12,fade:6,col:11394669}
function rlk:mboss/butterfly/fx/snd/wing_strike
playsound minecraft:block.cherry_leaves.break hostile @a[tag=player] ~ ~ ~ 0.8 1 0.27
