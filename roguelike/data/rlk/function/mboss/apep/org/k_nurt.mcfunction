# STUB (AP-CORE, ap_contract 1.6): the organism runtime; AP-REV replaces this file.
# Stationary; after its 20 t tell it links up to 3 basics within r 10 (tag rlk_mb_ap_buff);
# NURTURE_MODE A: itself immune (rlk_mb_ap_imm) while it holds a link.
execute if score @s apT matches ..19 run return 0
tag @e[type=minecraft:husk,tag=rlk_mb_ap_basic,distance=..10,limit=3,sort=nearest] add rlk_mb_ap_buff
tag @s remove rlk_mb_ap_imm
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_buff,distance=..10,limit=1] run tag @s add rlk_mb_ap_imm
