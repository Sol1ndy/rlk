# Reload: the framework values from the module's own state (init keeps live values; re-assert anyway).
scoreboard players set #bfDmgPct mb 100
scoreboard players set #mbCritAdd mb 0
scoreboard players set #mbHealPct mb 100
execute if score #bfBuff mb matches 1 run scoreboard players set #bfDmgPct mb 150
execute if score #bfBuff mb matches 1 run scoreboard players set #mbCritAdd mb 15
execute if score #bfCoc mb matches 1 run scoreboard players set #bfDmgPct mb 50
execute if score #bfCoc mb matches 1 run scoreboard players set #mbCritAdd mb -100
execute if score #bfCoc mb matches 1 run scoreboard players set #mbHealPct mb 60
