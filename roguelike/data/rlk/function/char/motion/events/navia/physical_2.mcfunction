function rlk:char/motion/audio/navia/physical_2
# Normal attack 2 (owner: na12; retimed to playback 100, 60 ticks): low re-cock, rising diagonal (hit 7), Geo spikes
# 8-9, skip-hop with the halberd overhead, low landing at 14 held to 29, a slow CCW turn back to IDLE_D at 60 (chain 14). Damage: generated combat/config/navia/physical_2
# (pmStrike = hit_ticks[0]). Fx: navia_fx/physical_2.
# Retime (Genshin recovery): the tail after the chain tick plays out to IDLE_D unless the player acts.
scoreboard players set @s cboIdle 0
execute if score @s pmTick matches 14.. if score @s pmVisible matches 1 unless score @s pmWantMode matches 0 run return run function rlk:char/motion/finish
