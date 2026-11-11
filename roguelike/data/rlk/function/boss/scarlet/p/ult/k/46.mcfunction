# ULT pattern tick 46
scoreboard players set #gau hr 0
function rlk:boss/scarlet/fx/hud/ovl {g:"white",in:0,hold:3,out:6}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:dust{color:[1.0,0.95,0.98],scale:1.0} ~ ~ ~ 8 1.5 8 0.2 100 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.1 ~ run function rlk:boss/scarlet/fx/p/burst_radial {r:60}
execute at @s run function rlk:boss/scarlet/fx/snd/ult_cut2
