# @s = a shielded basic whose pool breaks on this hit: the rest of the hit (in HP terms) goes on to its HP.
scoreboard players operation #apSd mb -= @s apShd
execute if score #elem tmp matches 1 run scoreboard players set #apY mb 150
execute if score #elem tmp matches 1 run scoreboard players operation #apSd mb *= #c100 mb
execute if score #elem tmp matches 1 run scoreboard players operation #apSd mb /= #apY mb
scoreboard players operation #apZ mb = @s apShd
function rlk:boss/apep/org/basic/shd_off
execute at @s positioned ~ ~0.8 ~ run function rlk:boss/apep/fx/p/shield_pop
execute at @s run function rlk:boss/apep/fx/snd/o3_pop
scoreboard players operation #dmg tmp = #apSd mb
execute if score #dmg tmp matches ..0 run scoreboard players set #mbAuxDone mb 1
