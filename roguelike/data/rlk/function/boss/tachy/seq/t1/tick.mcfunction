# T1 날개 전개 (PLAN §3: kneel, the cape splits into the wings, spread, gold flare, stand). @s = the body; #sq tk 1.. = the clip tick shown this game tick.
execute if score #sq tk matches 0 at @s run function rlk:boss/tachy/fx/snd/stagger
execute if score #sq tk matches 10 at @s run function rlk:boss/tachy/fx/snd/t1_split
execute if score #sq tk matches 10 at @s run function rlk:boss/tachy/fx/p/ember_burst
execute if score #sq tk matches 30 at @s run function rlk:boss/tachy/fx/snd/cape_gust
execute if score #sq tk matches 50 at @s run function rlk:boss/tachy/fx/snd/t1_flare
execute if score #sq tk matches 50 at @s run function rlk:boss/tachy/fx/p/wing_flare
execute if score #sq tk matches 70 at @s run function rlk:boss/tachy/fx/snd/step
execute if score #sq tk matches 80.. run scoreboard players set #sqdone tk 1
