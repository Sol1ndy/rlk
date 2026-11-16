# The immunity (mode A) and the cylinder follow the link count.
execute if score @s apSock matches 1.. run tag @s add rlk_mb_ap_imm
execute unless score @s apSock matches 1.. run tag @s remove rlk_mb_ap_imm
execute if score @s apSock matches 1.. unless entity @s[tag=rlk_mb_ap_ring] run function rlk:boss/apep/org/nurt/ring_on
execute unless score @s apSock matches 1.. if entity @s[tag=rlk_mb_ap_ring] run function rlk:boss/apep/org/nurt/ring_off
