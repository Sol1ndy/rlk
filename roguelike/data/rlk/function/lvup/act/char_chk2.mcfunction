scoreboard players set #pkIsChar tmp 0
$execute if data storage rlk:items registry.$(id).char run scoreboard players set #pkIsChar tmp 1
$data modify storage rlk:lvpick ch.id set from storage rlk:items registry.$(id).char
