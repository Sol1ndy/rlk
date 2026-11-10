# @s = groggy enemy (bal/uninstall): undo what the family changed on the entity, no sound, no redraw
scoreboard players set @s grgT 0
tag @s remove rlk_bal_grog
execute if score @s balC matches 1..2 run function rlk:bal/fam/noai_off
