# S3 groggy (@s = body, at it; #bfT 1..300; no tracking, nothing that moves her): dazed motes, the faint
# rings, the stirring before the turn.
scoreboard players operation #bfM mb = #bfT mb
scoreboard players operation #bfM mb %= #bfK10 mb
execute if score #bfM mb matches 0 if score #bfT mb matches 10..300 run function rlk:mboss/butterfly/seq_h/groggy/e0_10_10
scoreboard players operation #bfM mb = #bfT mb
scoreboard players operation #bfM mb %= #bfK40 mb
execute if score #bfM mb matches 0 if score #bfT mb matches 40..300 run function rlk:mboss/butterfly/seq_h/groggy/e1_40_40
execute if score #bfT mb matches 100 run return run function rlk:mboss/butterfly/seq_h/groggy/k/100
execute if score #bfT mb matches 200 run return run function rlk:mboss/butterfly/seq_h/groggy/k/200
execute if score #bfT mb matches 280 run return run function rlk:mboss/butterfly/seq_h/groggy/k/280
