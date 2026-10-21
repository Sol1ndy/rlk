# @s = a 파괴 broken before the blast: its blast hazard is cancelled; the burst; org_die.
scoreboard players operation #apX mb = @s apL
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_ohz] if score @s apL = #apX mb run kill @s
function rlk:boss/apep/om/destr/play/org_die
execute at @s positioned ~ ~0.6 ~ run function rlk:boss/apep/fx/p/org_burst
execute at @s run function rlk:boss/apep/fx/snd/org_kill
