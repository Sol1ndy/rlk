function rlk:char/motion/audio/navia/burst
# Burst (owner: burst), started by char/burst_wind (buT 34). The blast is not called here: burst_wind_tick runs
# burst_go when buT reaches 0 (clip tick 34), rotated as the locked basis. Lock and i-frames cover the cast.
# The clip owns the parasol fx (navia_fx/burst: cast, shoulder rest, flash, cosmetic barrage, put-away, halberd
# re-form) and the wind-up/put-away sounds (navia_audio/burst.py); the blast sound and support shells stay gameplay.
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 44
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 0 run scoreboard players set #pmInv tmp 44
execute if score @s pmTick matches 0 run scoreboard players operation @s dashInvT > #pmInv tmp
# Retime (108 ticks): the shoulder rest holds to 82 and the put-away ends at 100, halberd on the back from 101
# (Genshin v1/v6); the blast (34), lock and i-frames (44) do not move.
# Moving or jumping after the lock: quick stow instead of sliding the shoulder rest.
execute if score @s pmTick matches 45.. if score @s pmVisible matches 1 unless score @s pmWantMode matches 0 run return run function rlk:char/motion/sheath/abort
