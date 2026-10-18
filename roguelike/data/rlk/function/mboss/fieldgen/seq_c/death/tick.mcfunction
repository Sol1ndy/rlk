# S4 on the death clock (@s = body; #mbT = death clip tick 1 ..): flickers 6 / 12, drop 20, sink 40,
# land 62, the fade 80 with the scale-out (every card gone by 108 <= death_finish 110).
execute if score #mbT mb matches 6 run return run function rlk:mboss/fieldgen/seq_c/death/k/6
execute if score #mbT mb matches 12 run return run function rlk:mboss/fieldgen/seq_c/death/k/12
execute if score #mbT mb matches 20 run return run function rlk:mboss/fieldgen/seq_c/death/k/20
execute if score #mbT mb matches 40 run return run function rlk:mboss/fieldgen/seq_c/death/k/40
execute if score #mbT mb matches 62 run return run function rlk:mboss/fieldgen/seq_c/death/k/62
execute if score #mbT mb matches 80 run return run function rlk:mboss/fieldgen/seq_c/death/k/80
