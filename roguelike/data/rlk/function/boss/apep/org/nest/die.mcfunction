function rlk:boss/apep/om/nest/play/org_die
execute at @s positioned ~ ~1.2 ~ run function rlk:boss/apep/fx/p/org_burst
execute at @s run function rlk:boss/apep/fx/snd/org_kill
scoreboard players operation #apX mb = @s apL
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wlock] if score @s apL = #apX mb run kill @s
