# burst tick.
execute if score #fq5Pz mb matches 1 run function rlk:mboss/fieldgen/p/burst/resume
execute if score #fgPT mb matches 1..41 run return run function rlk:mboss/fieldgen/p/burst/d/1_41
execute if score #fgPT mb matches 44..130 run return run function rlk:mboss/fieldgen/p/burst/d/44_130
