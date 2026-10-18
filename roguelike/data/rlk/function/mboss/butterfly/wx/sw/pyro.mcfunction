# -> Pyro: the kit's magenta-pink rim pulse (2 cards, 10 small flames), a gold wing-span glow (#FAD77C),
# a magenta spark at each forewing tip; the soft whump + shimmer recipe (S6: about one real tick).
execute rotated as @s rotated ~ 0 positioned ~ ~2.8 ~ run function rlk:mboss/butterfly/fx/p/pyro_switch
execute rotated as @s rotated ~ 0 positioned ~ ~3.0 ~ run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1.5,s1:4.5,move:"0f,0f,0f",life:6,fade:3,col:16439164}
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.886f,0.431f,0.314f],scale:1.2} ~ ~ ~ 0.1 0.1 0.1 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.886f,0.431f,0.314f],scale:1.2} ~ ~ ~ 0.1 0.1 0.1 0 1 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/pyro_switch
