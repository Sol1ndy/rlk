# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# @s = body (phase 2, module tick): the stage stops while a service (fail / CS) runs; the organisms; the Heart
# limits (CS / failure strike); the waves (due on <= 1 alive or the wave clock; a due wave waits for the cap); the
# time-out.
execute unless score #apStage mb matches 1 run return 0
execute if score #apPid mb matches 1.. run return 0
scoreboard players add #apClk mb 1
scoreboard players add #apWT mb 1
scoreboard players set #apSlots mb 0
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_org] at @s run function rlk:boss/apep/org/tick
execute if score #apHt mb matches 10000.. run return run function rlk:boss/apep/svc/req_cs
execute if score #apHt mb matches ..0 run return run function rlk:boss/apep/svc/req_fail
scoreboard players set #apAlive mb 0
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_org] run scoreboard players add #apAlive mb 1
function rlk:boss/apep/rev/wave_due
execute if score #apClk mb matches 2000.. run function rlk:boss/apep/rev/timeout
