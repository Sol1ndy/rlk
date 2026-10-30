scoreboard players add #fgT mb 1
execute if score #fgT mb matches 5 run function rlk:mboss/fieldgen/brk/burst
function rlk:mboss/fieldgen/seq_f/brk/tick
execute if score #fgT mb matches 40.. run function rlk:mboss/fieldgen/groggy/begin
