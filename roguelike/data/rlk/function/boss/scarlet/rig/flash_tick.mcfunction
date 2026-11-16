# Internal: counts the flash down.
scoreboard players remove @s hrRigF 1
execute if score @s hrRigF matches ..0 run function rlk:boss/scarlet/rig/flash_off
