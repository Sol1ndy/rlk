# E on the intro clock (@s = body; #mbT = entrance clip tick + 1): clank 16, pods 20,
# unfold 30, eye 60, turn 60, rise 64, online at 94 (the fight starts there).
execute if score #mbT mb matches 14..31 run return run function rlk:mboss/fieldgen/seq_c/entrance/d/13_30
execute if score #mbT mb matches 39..95 run return run function rlk:mboss/fieldgen/seq_c/entrance/d/38_94
