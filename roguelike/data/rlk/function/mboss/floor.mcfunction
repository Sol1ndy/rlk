# @s = the body inside combat/apply_mods, after the module's incoming hook (cb/inc/<id>; modules never call this).
# #mbFloor mb >= 1 (absolute HP, set by the module): #mbFloorRaw = the unclamped #dmg; a hit with mhpC - raw <= #mbFloor
# sets #mbFloorHit 1 (the module clears it); #dmg = max(0, min(#dmg, mhpC - #mbFloor)). True damage never gets here.
execute unless score #mbFloor mb matches 1.. run return 0
scoreboard players operation #mbFloorRaw mb = #dmg tmp
scoreboard players operation #t mb = @s mhpC
scoreboard players operation #t mb -= #dmg tmp
execute if score #t mb <= #mbFloor mb run scoreboard players set #mbFloorHit mb 1
scoreboard players operation #t mb = @s mhpC
scoreboard players operation #t mb -= #mbFloor mb
scoreboard players operation #dmg tmp < #t mb
execute if score #dmg tmp matches ..-1 run scoreboard players set #dmg tmp 0
