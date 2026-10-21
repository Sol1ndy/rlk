# From rlk:uninstall: remove everything the mid-boss framework created (arena blocks stay); every module's
# uninstall hook first (their own objectives and leftovers).
function rlk:mboss/cleanup
function rlk:mboss/d/uninstall
# low gravity (mboss/lowg_on): the modifiers off every player and every entity still tagged
execute as @a run function rlk:mboss/lowg_rem
execute as @e[tag=rlk_lowg] run function rlk:mboss/lowg_rem
kill @e[tag=rlk_mb_body]
kill @e[tag=rlk_mb_aux]
bossbar remove rlk:mboss
bossbar remove rlk:mboss_state
bossbar remove rlk:mboss_sub
execute in minecraft:overworld run forceload remove 176 -16 223 31
# chapter mode: the running arena job, every arena's forceload, the music, chapter storage
function rlk:mboss/arena/abort
schedule clear rlk:mboss/arena/job_tick
function rlk:mboss/music/stop
execute in minecraft:overworld run function rlk:mboss/ar/az_cavern/fl_off
execute in minecraft:overworld run function rlk:mboss/ar/ap_oasis/fl_off
execute in minecraft:overworld run function rlk:mboss/ar/cp_test/fl_off
data remove storage rlk:mboss reg
data remove storage rlk:mboss byid
data remove storage rlk:mboss met
data remove storage rlk:mboss tlast
data remove storage rlk:mboss creg
data remove storage rlk:mboss cbyid
data remove storage rlk:mboss cprep
data remove storage rlk:mboss cbpeek
data remove storage rlk:mboss cbl
data remove storage rlk:mboss cbg
data remove storage rlk:mboss tch
data remove storage rlk:mboss pxq
data remove storage rlk:mboss arsw
data remove storage rlk:mboss plp
data remove storage rlk:mboss arjob
data remove storage rlk:mboss built_az_cavern
data remove storage rlk:mboss look_az_cavern
data remove storage rlk:mboss built_ap_oasis
data remove storage rlk:mboss look_ap_oasis
data remove storage rlk:mboss built_cp_test
data remove storage rlk:mboss look_cp_test
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
scoreboard objectives remove mbHzND
scoreboard objectives remove mbHzRA
scoreboard objectives remove mbHzRT
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
scoreboard objectives remove mbRes0
scoreboard objectives remove mbRes1
scoreboard objectives remove mbRes2
scoreboard objectives remove mbRes3
scoreboard objectives remove mbRes4
scoreboard objectives remove mbRes5
scoreboard objectives remove mbRes6
scoreboard objectives remove mbRes7
scoreboard objectives remove mbRes8
scoreboard objectives remove mbHzNR
scoreboard objectives remove mbHzSG
scoreboard objectives remove mbPjND
scoreboard objectives remove mbPjNR
scoreboard objectives remove mbPart
scoreboard objectives remove mbHzPm
scoreboard objectives remove mbHzPmL
