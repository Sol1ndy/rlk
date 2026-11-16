function rlk:char/motion/audio/navia/physical_2
# Normal attack 2 (owner: na12; retimed at playback 100, played at 130 since D12, 60 ticks): low re-cock, rising diagonal (hit 7), Geo spikes
# 8-9, skip-hop with the halberd overhead, low landing at 14 held to 29, a slow CCW turn back to IDLE_D at 60 (chain 14). Damage: generated combat/config/navia/physical_2
# (pmStrike = hit_ticks[0]). Fx: navia_fx/physical_2.
# Frames 0-2 hold the halberd raised behind her right side (re-cock low from 3): a chain shows its first frame through a
# 1-tick client blend from whatever NA1 shows, and from these the halberd stays above the floor from every NA1 tick.
# Retime (Genshin recovery): the tail after the chain tick plays out to IDLE_D unless the player acts.
scoreboard players set @s cboIdle 0
# Moving or jumping ends it once a chained click would be accepted (#pmChainOpen, see physical_1).
# Before that tick the swing (player/swing/tick) halves walking (shoulder view) and blocks jumping; a jump from then on also
# restarts the string at NA1 (player/swing/jump).
execute if score @s pmTick matches 14.. if score #pmChainOpen tmp matches 1 if score @s pmVisible matches 1 unless score @s pmWantMode matches 0 run return run function rlk:char/motion/finish
