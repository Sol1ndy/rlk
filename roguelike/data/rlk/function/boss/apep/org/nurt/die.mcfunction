# @s = a 양육 broken (killed, or its self-destruct): nurt_die (17 t); its basics lose the buff.
function rlk:boss/apep/om/nurt/play/nurt_die
tag @s remove rlk_mb_ap_imm
execute if entity @s[tag=rlk_mb_ap_ring] run function rlk:boss/apep/org/nurt/ring_off
execute if entity @s[tag=rlk_mb_ap_selfd] at @s positioned ~ ~1.8 ~ run function rlk:boss/apep/fx/p/nurt_burst
execute if entity @s[tag=rlk_mb_ap_selfd] at @s run function rlk:boss/apep/fx/snd/o5_destruct
execute unless entity @s[tag=rlk_mb_ap_selfd] at @s positioned ~ ~1.2 ~ run function rlk:boss/apep/fx/p/org_burst
execute unless entity @s[tag=rlk_mb_ap_selfd] at @s run function rlk:boss/apep/fx/snd/org_kill
scoreboard players operation #apX mb = @s apL
scoreboard players set @s apSock 0
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_buff] if score @s apL = #apX mb run function rlk:boss/apep/org/basic/buff_off
