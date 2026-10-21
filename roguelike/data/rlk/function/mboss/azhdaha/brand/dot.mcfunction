# @s = player: one DoT tick through mboss/pl_dot (non-lethal, shields absorb, no defence, i-frames ignored).
scoreboard players set @s azBrC 20
scoreboard players set #mbDotPct mb 5
execute if score @s azBrE matches 4 if score @s azBrS matches 2 run scoreboard players set #mbDotPct mb 7
execute if score @s azBrE matches 4 if score @s azBrS matches 3.. run scoreboard players set #mbDotPct mb 10
scoreboard players operation #mbDotEl mb = @s azBrE
scoreboard players set #mbDotLethal mb 0
function rlk:mboss/pl_dot
function rlk:mboss/azhdaha/fx/snd/brand_tick
scoreboard players remove @s azBrT 1
# Cryo: a tick without a new Cryo strike since the previous tick drops one stack (3 -> 2 -> 1)
execute if score @s azBrE matches 4 unless score #azBrCs mb matches 1 if score @s azBrS matches 2.. run scoreboard players remove @s azBrS 1
scoreboard players set #azBrCs mb 0
scoreboard players set #azHudQ mb 1
execute if score @s azBrT matches ..0 run function rlk:mboss/azhdaha/brand/clear
