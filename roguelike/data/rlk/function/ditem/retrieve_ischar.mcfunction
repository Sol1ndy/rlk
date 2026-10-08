scoreboard players set #isCh tmp 0
$execute if data storage rlk:items registry.$(id).char run scoreboard players set #isCh tmp 1
$data modify storage rlk:dtmp ch.id set from storage rlk:items registry.$(id).char
