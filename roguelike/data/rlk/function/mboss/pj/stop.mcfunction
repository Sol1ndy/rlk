# End of the outward flight. A returning prop turns around instead.
$scoreboard players set #pjEv mb $(ev)
execute if score @s mbPjRet matches 1 run return run scoreboard players set @s mbPjRet 2
function rlk:mboss/pj/finish
