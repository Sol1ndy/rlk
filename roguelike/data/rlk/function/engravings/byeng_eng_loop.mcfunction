execute unless data storage rlk:engravings beq[0] run return 0
data modify storage rlk:engravings bcur.e set from storage rlk:engravings beq[0]
function rlk:engravings/byeng_add with storage rlk:engravings bcur
data remove storage rlk:engravings beq[0]
function rlk:engravings/byeng_eng_loop
