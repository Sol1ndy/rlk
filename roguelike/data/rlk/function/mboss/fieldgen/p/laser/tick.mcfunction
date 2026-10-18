# laser tick.
execute if score #fq3Pz mb matches 1 run function rlk:mboss/fieldgen/p/laser/resume
execute if score #fgPT mb matches 25..156 run function rlk:mboss/fieldgen/p/laser/aim
execute if score #fgPT mb matches 3..64 run return run function rlk:mboss/fieldgen/p/laser/d/3_64
execute if score #fgPT mb matches 74..174 run return run function rlk:mboss/fieldgen/p/laser/d/74_174
