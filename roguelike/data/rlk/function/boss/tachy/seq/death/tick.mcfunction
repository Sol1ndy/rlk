# Death (PLAN §3: knees buckle, sword planted, visor fades, wings sag, collapse, ash). @s = the body; #sq tk 1.. = the clip tick shown this game tick.
execute if score #sq tk matches 20 at @s run function rlk:boss/tachy/fx/snd/death_knee
execute if score #sq tk matches 36 at @s run function rlk:boss/tachy/fx/snd/chop
execute if score #sq tk matches 100 at @s run function rlk:boss/tachy/fx/p/dust_ring {r:20}
execute if score #sq tk matches 116 at @s run function rlk:boss/tachy/fx/snd/death_ash
execute if score #sq tk matches 116 at @s run function rlk:boss/tachy/fx/p/ember_burst
execute if score #sq tk matches 130.. run scoreboard players set #sqdone tk 1
