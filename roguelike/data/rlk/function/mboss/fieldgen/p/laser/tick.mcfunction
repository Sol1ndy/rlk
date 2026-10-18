# laser tick.
execute if score #fq3Pz mb matches 1 run function rlk:mboss/fieldgen/p/laser/resume
execute if score #fgPT mb matches 23..154 run function rlk:mboss/fieldgen/p/laser/aim
execute if score #fgPT mb matches 3..62 run return run function rlk:mboss/fieldgen/p/laser/d/3_62
execute if score #fgPT mb matches 72..165 run return run function rlk:mboss/fieldgen/p/laser/d/72_165
