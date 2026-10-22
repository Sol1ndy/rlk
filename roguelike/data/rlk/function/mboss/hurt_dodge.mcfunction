scoreboard players add #mbDodgeEv mb 1
execute if score #mbSrcIn mb matches 2 run return run scoreboard players set #mbDodgeOk mb 1
execute unless score #mbSrcIn mb matches 1 run return 0
execute if score @s mbHzRA matches 0 if score @s mbHzW matches 12.. if score @s mbHzND matches 0 run scoreboard players set #mbDodgeOk mb 1
