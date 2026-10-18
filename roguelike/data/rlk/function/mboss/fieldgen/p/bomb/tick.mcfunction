# bomb tick.
execute if score #fq1Pz mb matches 1 run function rlk:mboss/fieldgen/p/bomb/resume
execute if score #fgPT mb matches 1..9 run function rlk:mboss/fieldgen/rig/face/track
execute if score #fgPT mb matches 8..35 run return run function rlk:mboss/fieldgen/p/bomb/d/8_35
execute if score #fgPT mb matches 36..94 run return run function rlk:mboss/fieldgen/p/bomb/d/36_94
