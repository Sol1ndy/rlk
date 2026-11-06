# @s = a basic broken by the player: the burst, its death clip; a buffed one costs its 양육 (link lost).
function rlk:boss/apep/om/basic/play/org_die
execute at @s positioned ~ ~0.6 ~ run function rlk:boss/apep/fx/p/org_burst
execute at @s run function rlk:boss/apep/fx/snd/org_kill
execute if entity @s[tag=rlk_mb_ap_shd] run function rlk:boss/apep/org/basic/shd_off
execute if score @s apL matches 1.. run function rlk:boss/apep/org/nurt/lost_of
