# @s = a new enemy, at @s (mob/setup, after rlk_mob): its tier, a full gauge and (normal / elite) the pip row under the
# head bar. Excluded (no gauge, never groggy): mechanic objects and stand-ins (boss aux / hit objects and proxies,
# Raiden objects, spore pods, cicin summons, lobby dummies); pets never reach mob/setup.
# A mob set up again (a burrower surfacing) keeps its gauge and gets its row back.
execute if score @s balMax matches 0.. run return run function rlk:bal/re_init
scoreboard players set @s balMax 0
scoreboard players set @s balC 0
scoreboard players set @s bal 0
scoreboard players set @s balT 0
scoreboard players set @s grgT 0
execute if entity @s[tag=rlk_mb_aux] run return 0
execute if entity @s[tag=rlk_mb_hit] run return 0
execute if entity @s[tag=rlk_mb_px] run return 0
execute if entity @s[tag=rlk_rd_object] run return 0
execute if entity @s[tag=rlk_c3pod] run return 0
execute if entity @s[tag=rlk_cm_ci] run return 0
execute if entity @s[tag=rlk_lobby] run return 0
execute if entity @s[tag=rlk_pet] run return 0
# bosses: a registry boss only when its module implements the balance hooks (registry "bal", mboss/d/bal_has)
execute if entity @s[tag=rlk_mb_body] unless function rlk:mboss/d/bal_has run return run data remove storage rlk:bal brow
execute if entity @s[tag=rlk_mb_body] run scoreboard players set @s balC 3
execute if entity @s[tag=rlk_raiden] run scoreboard players set @s balC 3
execute if score @s balC matches 0 if entity @s[tag=rlk_c2e] run scoreboard players set @s balC 2
execute if score @s balC matches 0 if entity @s[tag=rlk_c3e] run scoreboard players set @s balC 2
execute if score @s balC matches 0 run scoreboard players set @s balC 1
execute if score @s balC matches 1 run scoreboard players operation @s balMax = #pips1 bal
execute if score @s balC matches 2 run scoreboard players operation @s balMax = #pips2 bal
execute if score @s balC matches 3 run scoreboard players operation @s balMax = #pips3 bal
scoreboard players operation @s bal = @s balMax
scoreboard players set @s balF 0
scoreboard players set @s balQ 0
scoreboard players set @s balX 0
execute if score @s balC matches 1..2 run function rlk:bal/ui/row_new
function rlk:bal/ui/draw
