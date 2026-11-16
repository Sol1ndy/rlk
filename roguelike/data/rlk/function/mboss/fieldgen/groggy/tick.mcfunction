scoreboard players add #fgT mb 1
function rlk:mboss/fieldgen/seq_f/groggy/tick
execute if score #fgT mb matches 200.. run function rlk:mboss/fieldgen/recover/begin
