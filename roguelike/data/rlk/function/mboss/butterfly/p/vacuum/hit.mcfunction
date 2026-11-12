# The blade hit the player: a lime spark there; it flies on harmlessly to the wall.
scoreboard players set #pjKeep mb 1
execute at @e[tag=rlk_body,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"~ ~1 ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.4,s1:1.4,move:"0f,0f,0f",life:4,fade:2,col:14088121}
execute at @e[tag=rlk_body,limit=1] run particle minecraft:crit ~ ~1 ~ 0.3 0.5 0.3 0.3 8 force @a[tag=player]
