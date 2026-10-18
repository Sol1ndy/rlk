# vacuum clock 16
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1.0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/p/vac_stomp
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"flame_tongue",pos:"^ ^ ^1.0",rot:"~ ~",bb:"vertical",roll:0,spin:0,s0:0.4,s1:1.2,move:"0f,0f,0f",life:4,fade:2,col:16777215}
execute at @s rotated as @s rotated ~ 0 run particle minecraft:block{block_state:"minecraft:mossy_cobblestone"} ^ ^0.2 ^1.0 0.4 0.2 0.4 0.2 8 force @a[tag=player]
