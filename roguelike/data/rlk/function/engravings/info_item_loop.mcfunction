execute unless data storage rlk:eng sq[0] run return 0
execute if score #slot eng matches 27.. run return 0
function rlk:engravings/info_item with storage rlk:eng sq[0]
scoreboard players add #slot eng 1
data remove storage rlk:eng sq[0]
function rlk:engravings/info_item_loop
