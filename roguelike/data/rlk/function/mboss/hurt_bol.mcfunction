# ar FN-1 (scratchpad ar/contract.md 3.1): the rest of mboss/hurt for a Bond-of-Life hit, @s = its hazard marker or
# projectile prop (mbBol 1..100; #mbBolIn = mbBol for this call). The raw damage x #mbBolRe mb / 100 (the module's
# multiplier, unset = 100) before the hit; after a hit that reached the player (not dodged; a refused one never gets
# here) #mbHitBol mb = mbBol (the module reads and clears it). #mbBolIn is gone again afterwards.
scoreboard players operation #mbBolIn mb = @s mbBol
execute unless score #mbBolRe mb matches 0.. run scoreboard players set #mbBolRe mb 100
scoreboard players operation #cmDmg tmp *= #mbBolRe mb
scoreboard players operation #cmDmg tmp /= #c100 mb
execute if score #cmDmg tmp matches ..0 run scoreboard players set #cmDmg tmp 1
scoreboard players operation #cmLv tmp = #mbLv mb
scoreboard players operation #cmKB tmp = #mbKB mb
kill @e[tag=rlk_plkb_source]
execute if score #cmKB tmp matches 1.. run function rlk:mboss/kb_src
execute unless score #mbNoDodge mb matches 1 as @a[tag=player,limit=1] run function rlk:cm/hit_pl2
# #mbNoDodge mb 1 (a #hzNoDodge hazard): dash i-frames do not help this hit
execute if score #mbNoDodge mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/hurt_nd
scoreboard players set #mbNRNow mb 0
kill @e[tag=rlk_plkb_source]
scoreboard players set #mbKBDir mb 0
function rlk:mboss/hurt_ev
execute if score #dodged tmp matches 0 run scoreboard players operation #mbHitBol mb = #mbBolIn mb
scoreboard players reset #mbBolIn mb
