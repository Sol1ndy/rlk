# T2 심연 (PLAN §3: stagger, red visor, tendrils, darkness + the abyss arena, rise). @s = the body; #sq tk 1.. = the clip tick shown this game tick.
execute if score #sq tk matches 0 at @s run function rlk:boss/tachy/fx/snd/stagger
execute if score #sq tk matches 20 at @s run function rlk:boss/tachy/fx/snd/t2_flare
execute if score #sq tk matches 20 at @s run function rlk:boss/tachy/fx/p/core_flare {c:2}
execute if score #sq tk matches 36 at @s run function rlk:boss/tachy/fx/p/core_burst
execute if score #sq tk matches 50 at @s run function rlk:boss/tachy/fx/snd/t2_dark
execute if score #sq tk matches 50 run effect give @a[tag=player] minecraft:blindness 1 0 true
execute if score #sq tk matches 50 run function rlk:mboss/arena/tk_lift/look/abyss
execute if score #sq tk matches 90 at @s run function rlk:boss/tachy/fx/p/wing_flare
execute if score #sq tk matches 110.. run scoreboard players set #sqdone tk 1
