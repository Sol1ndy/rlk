# @s = a basic: the 수호 shield (plan 7.6.6): pool = 5 x its max HP, the overlay, the pop.
execute if entity @s[tag=rlk_mb_ap_shd] run return 0
tag @s add rlk_mb_ap_shd
scoreboard players operation @s apShd = @s mhpM
scoreboard players set #apY mb 5
scoreboard players operation @s apShd *= #apY mb
function rlk:boss/apep/om/basic/shield/on
execute at @s positioned ~ ~0.8 ~ run function rlk:boss/apep/fx/p/shield_pop
execute at @s run function rlk:boss/apep/fx/snd/o3_pop
