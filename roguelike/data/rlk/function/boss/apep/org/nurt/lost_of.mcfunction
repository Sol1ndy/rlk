# @s = a linked basic that died or was swallowed: its 양육 (apL) loses the link and 40 % of its max HP (the module break
# on the 3rd: "자멸").
scoreboard players operation #apX mb = @s apL
scoreboard players set @s apL 0
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_nurt,tag=!rlk_mb_ap_dying] if score @s apL = #apX mb run function rlk:boss/apep/org/nurt/loss
