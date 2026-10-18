# Reload: the framework values from the module's own state (init keeps live values; re-assert anyway).
scoreboard players set #bfDmgPct mb 100
scoreboard players set #mbCritAdd mb 0
scoreboard players set #mbCritDmgAdd mb 0
scoreboard players set #mbHealPct mb 100
execute if score #bfBuff mb matches 1 run scoreboard players set #mbCritAdd mb 15
execute if score #bfBuff mb matches 1 run scoreboard players set #mbCritDmgAdd mb 50
execute if score #bfCoc mb matches 1 run scoreboard players set #bfDmgPct mb 50
execute if score #bfCoc mb matches 1 run scoreboard players set #mbCritAdd mb -100
execute if score #bfCoc mb matches 1 run scoreboard players set #mbHealPct mb 60
# the cure meter (#bfCure) is kept; its target and readout again
execute if score #bfCoc mb matches 1 as @a[tag=player,limit=1] run function rlk:mboss/butterfly/coc/meter
# the kit's HUD badges from the module state (storage rlk:bfkit survives a reload; re-assert anyway)
function rlk:mboss/butterfly/fx/hud/clear
execute if score #bfCoc mb matches 1 run function rlk:mboss/butterfly/fx/hud/coc_on
execute if score #bfBuff mb matches 1 run function rlk:mboss/butterfly/fx/hud/buff_on
