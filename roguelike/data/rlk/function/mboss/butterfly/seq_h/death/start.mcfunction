# S4 at death_start (@s = body; the core has cancelled everything): the hit flash, a white burst at her core, the
# death recipe (crystal, beacon, wind; no voices).
function rlk:mboss/butterfly/rig_stub/flash
execute if score #bfForm mb matches 1 at @s rotated as @s rotated ~ 0 positioned ^ ^2.1 ^ run function rlk:mboss/butterfly/fx/card {kind:"burst",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.8,s1:2.6,move:"0f,0f,0f",life:4,fade:2,col:16777215}
execute if score #bfForm mb matches 2 at @s rotated as @s rotated ~ 0 positioned ^ ^3.2 ^ run function rlk:mboss/butterfly/fx/card {kind:"burst",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.8,s1:2.6,move:"0f,0f,0f",life:4,fade:2,col:16777215}
execute at @s run particle minecraft:flash{color:[0.95,1.0,0.9,0.9]} ~ ~2.0 ~ 0 0 0 0 1 force @a[tag=player]
execute at @s run function rlk:mboss/butterfly/fx/snd/death
