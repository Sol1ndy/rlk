# S4 on the death clock (@s = body; #mbT = death clip tick 1 ..): flickers 6 / 12, drop 20, sink 40,
# land 62, the fades 70 / 82 (every card gone by 110 <= death_finish 110).
execute if score #mbT mb matches 6..20 run return run function rlk:mboss/fieldgen/seq_c/death/d/6_20
execute if score #mbT mb matches 40..82 run return run function rlk:mboss/fieldgen/seq_c/death/d/40_82
