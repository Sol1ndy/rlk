# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# @s = an organism inside combat/apply (#dmg tmp after RES, #elem tmp; the core's aux_hit made an immune 양육 take
# nothing first). A shielded basic (수호, plan 7.6.6): the pool apShd (= 5 x its max HP) absorbs first, Pyro x1.5 against it;
# the absorbed part shows sky-blue with the shield sound (#mbAuxDone 1); a break pops the overlay and passes the rest on.
execute unless entity @s[tag=rlk_mb_ap_org] run return 0
execute unless entity @s[tag=rlk_mb_ap_shd] run return 0
execute unless score @s apShd matches 1.. run return 0
scoreboard players operation #apSd mb = #dmg tmp
execute if score #elem tmp matches 1 run scoreboard players set #apY mb 150
execute if score #elem tmp matches 1 run scoreboard players operation #apSd mb *= #apY mb
execute if score #elem tmp matches 1 run scoreboard players operation #apSd mb /= #c100 mb
execute if score #apSd mb matches ..0 run return 0
execute if score #apSd mb >= @s apShd run return run function rlk:boss/apep/org/basic/shd_break
scoreboard players operation @s apShd -= #apSd mb
function rlk:boss/apep/org/basic/shd_num
execute positioned ~ ~1 ~ run function rlk:boss/apep/fx/snd/shield_hit
scoreboard players set #mbAuxDone mb 1
