# Internal: counts the flash down.
scoreboard players remove @s knRigF 1
execute if score @s knRigF matches ..0 run function rlk:boss/arlecchino/rig/flash_off
