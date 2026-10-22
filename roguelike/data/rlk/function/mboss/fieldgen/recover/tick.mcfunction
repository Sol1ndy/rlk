scoreboard players add #fgT mb 1
execute if score #fgT mb matches 6 run function rlk:mboss/fieldgen/seq_f/recover/flip
execute if score #fgT mb matches 15.. run function rlk:mboss/fieldgen/recover/end
