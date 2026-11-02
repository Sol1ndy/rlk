# ar FN-1: the rest of hz/hurt_pm for a Bond-of-Life per-mille hazard (@s, mbBol 1..100; #mbBolIn = mbBol for this
# call): the per mille x #mbBolRe mb / 100 (unset = 100, at least 1), the pl_dot, the hit event and #mbHitBol mb = mbBol
# (the dodge returned before).
scoreboard players operation #mbBolIn mb = @s mbBol
execute unless score #mbBolRe mb matches 0.. run scoreboard players set #mbBolRe mb 100
scoreboard players operation #mbDotPct mb = @s mbHzPm
scoreboard players operation #mbDotPct mb *= #mbBolRe mb
scoreboard players operation #mbDotPct mb /= #c100 mb
execute if score #mbDotPct mb matches ..0 run scoreboard players set #mbDotPct mb 1
scoreboard players operation #mbDotEl mb = @s mbHzE
scoreboard players operation #mbDotLethal mb = @s mbHzPmL
function rlk:mboss/pl_dot
scoreboard players operation #cmEl tmp = @s mbHzE
function rlk:mboss/hurt_ev
scoreboard players operation #mbHitBol mb = #mbBolIn mb
scoreboard players reset #mbBolIn mb
scoreboard players operation #g mb = @s mbHzG
execute if score #g mb matches 1.. run function rlk:mboss/grp_mark
