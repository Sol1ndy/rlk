# ambient_p1 at each player every 10 t of the module clock (#t = #clk).
scoreboard players operation #t hr %= #c10 hr
execute if score #t hr matches 0 at @a[tag=player] run function rlk:boss/scarlet/fx/p/ambient_p1
