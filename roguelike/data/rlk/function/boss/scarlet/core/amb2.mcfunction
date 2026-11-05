# ambient_p2 at each player every 6 t of the module clock (#t = #clk).
scoreboard players set #t2 hr 6
scoreboard players operation #t hr %= #t2 hr
execute if score #t hr matches 0 at @a[tag=player] run function rlk:boss/scarlet/fx/p/ambient_p2
