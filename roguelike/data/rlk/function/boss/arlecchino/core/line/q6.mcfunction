# The dialog line of Q6 (@s = body): one of api.LINE_OF (random), #lines = when.
scoreboard players operation #lines kn = #clk kn
execute store result score #t kn run random value 0..2
execute if score #t kn matches 0 run function rlk:boss/arlecchino/fx/hud/line {id:15}
execute if score #t kn matches 1 run function rlk:boss/arlecchino/fx/hud/line {id:16}
execute if score #t kn matches 2 run function rlk:boss/arlecchino/fx/hud/line {id:17}
