# From rlk:uninstall: remove everything the mid-boss framework created (arena blocks stay); every module's
# uninstall hook first (their own objectives and leftovers).
function rlk:mboss/cleanup
function rlk:mboss/d/uninstall
kill @e[tag=rlk_mb_body]
kill @e[tag=rlk_mb_aux]
bossbar remove rlk:mboss
bossbar remove rlk:mboss_state
bossbar remove rlk:mboss_sub
execute in minecraft:overworld run forceload remove 176 -16 223 31
data remove storage rlk:mboss reg
data remove storage rlk:mboss byid
data remove storage rlk:mboss met
data remove storage rlk:mboss tlast
scoreboard objectives remove mb
scoreboard objectives remove mres
scoreboard objectives remove pkMb
scoreboard objectives remove mbHzK
scoreboard objectives remove mbHzT
scoreboard objectives remove mbHzW
scoreboard objectives remove mbHzA
scoreboard objectives remove mbHzL
scoreboard objectives remove mbHzD
scoreboard objectives remove mbHzE
scoreboard objectives remove mbHzB
scoreboard objectives remove mbHzKD
scoreboard objectives remove mbHzS
scoreboard objectives remove mbHzV
scoreboard objectives remove mbHzI
scoreboard objectives remove mbHzR
scoreboard objectives remove mbHzR0
scoreboard objectives remove mbHzC
scoreboard objectives remove mbHzAng
scoreboard objectives remove mbHzRR
scoreboard objectives remove mbHzRI
scoreboard objectives remove mbHzLo
scoreboard objectives remove mbHzHi
scoreboard objectives remove mbHzHW
scoreboard objectives remove mbHzFX
scoreboard objectives remove mbHzFZ
scoreboard objectives remove mbHzY0
scoreboard objectives remove mbHzY1
scoreboard objectives remove mbHzHit
scoreboard objectives remove mbHzCol
scoreboard objectives remove mbHzG
scoreboard objectives remove mbPjV
scoreboard objectives remove mbPjT
scoreboard objectives remove mbPjL
scoreboard objectives remove mbPjD
scoreboard objectives remove mbPjE
scoreboard objectives remove mbPjB
scoreboard objectives remove mbPjR
scoreboard objectives remove mbPjHit
scoreboard objectives remove mbPjRet
scoreboard objectives remove mbPjW
scoreboard objectives remove mbPjK
scoreboard objectives remove mbPjG
scoreboard objectives remove mbPlT
scoreboard objectives remove mbPlF
scoreboard objectives remove mbMvK
scoreboard objectives remove mbMvT
scoreboard objectives remove mbMvN
scoreboard objectives remove mbMvH
scoreboard objectives remove mbMvX0
scoreboard objectives remove mbMvY0
scoreboard objectives remove mbMvZ0
scoreboard objectives remove mbMvX1
scoreboard objectives remove mbMvY1
scoreboard objectives remove mbMvZ1
scoreboard objectives remove mbT
scoreboard objectives remove mbS
scoreboard objectives remove mbId
