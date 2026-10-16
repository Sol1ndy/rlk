function rlk:char/motion/audio/navia/burst
# Burst (owner: burst), started by char/burst_wind (buT 34). The blast is not called here: burst_wind_tick runs
# burst_go when buT reaches 0 (clip tick 34), rotated as the locked basis. Lock and i-frames cover the cast.
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 44
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 0 run scoreboard players set #pmInv tmp 44
execute if score @s pmTick matches 0 run scoreboard players operation @s dashInvT > #pmInv tmp
