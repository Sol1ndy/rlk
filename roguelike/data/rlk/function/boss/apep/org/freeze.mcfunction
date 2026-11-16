# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# Pause in phase 2: the organisms are NoAI husks stepped only by the module tick (off while paused). The walls
# are cleared by wall/clear; a 둥지 in its cast goes back to flying and re-casts later.
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_nest,scores={apS=2}] run function rlk:boss/apep/org/nest/abort
scoreboard players set #apSlots mb 0
