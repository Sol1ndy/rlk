# Internal: counts the flash down.
scoreboard players remove @s tkRigF 1
execute if score @s tkRigF matches ..0 run function rlk:boss/tachy/rig/flash_off
