# End of the outward flight (ev 1 wall, 2 life over). A returning prop reports it and turns around.
$scoreboard players set #pjEv mb $(ev)
execute if score @s mbPjRet matches 1 run return run function rlk:mboss/pj/turn
function rlk:mboss/pj/finish
