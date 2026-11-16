# Returning prop at the end of its outward flight: event 1/2 with #pjKeep 1 preset (fly back); 0 = removed.
# The return leg may last as long as the outward flight plus 2 s (mbPjL = 2 x elapsed + 40), then it
# ends with event 3 wherever the prop is (the body may have moved away faster than the prop flies).
scoreboard players set #pjKeep mb 1
function rlk:mboss/d/pj_end
execute if score #pjKeep mb matches 0 run return run kill @s
scoreboard players set @s mbPjRet 2
scoreboard players operation @s mbPjL = @s mbPjT
scoreboard players operation @s mbPjL += @s mbPjT
scoreboard players add @s mbPjL 40
