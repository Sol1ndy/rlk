# E on the intro clock (@s = body; #mbT = entrance clip tick + 1): clank 16, pods 24,
# unfold 28, eye 54, turn 60, rise 80, online at 110 (the fight starts there).
execute if score #mbT mb matches 14..37 run return run function rlk:mboss/fieldgen/seq_c/entrance/d/13_36
execute if score #mbT mb matches 39..111 run return run function rlk:mboss/fieldgen/seq_c/entrance/d/38_110
