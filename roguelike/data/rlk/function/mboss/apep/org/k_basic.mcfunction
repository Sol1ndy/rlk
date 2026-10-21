# STUB (AP-CORE, ap_contract 1.6): the organism runtime; AP-REV replaces this file.
# 0 emerging (30 t), 1 walking to the Heart, 2 at its range: an attack every 40 t (ranged 50 t) while
# holding one of the 3 slots.
execute if score @s apS matches 0 if score @s apT matches 30.. run scoreboard players set @s apS 1
execute if score @s apS matches 0 run return 0
execute if score @s apS matches 1 run return run function rlk:mboss/apep/org/b_walk
function rlk:mboss/apep/org/b_attack
