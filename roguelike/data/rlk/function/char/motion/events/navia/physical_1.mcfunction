function rlk:char/motion/audio/navia/physical_1
# Normal attack 1 (owner: na12; retimed to playback 100, 55 ticks): pivot wind-up, rising loop sweep across the front,
# hit 9, halberd head thuds on the floor at 15 and hangs there to 28, slow turn back, IDLE_D at 55 (chain 14). Damage is not called here: combat/request queued it from the generated
# combat/config/navia/physical_1 (pmStrike = hit_ticks[0]); motion/event fires combat/first on that tick.
# Fx: navia_fx/physical_1 (started with the clip).
# Retime (Genshin recovery): the tail after the chain tick plays out to IDLE_D unless the player acts.
# Keep the string alive while the tail plays (player/tick resets comboStep after 20 idle ticks).
scoreboard players set @s cboIdle 0
# Moving or jumping from the chain tick on ends the recovery (Genshin walk-cancel); drawn locomotion takes over.
execute if score @s pmTick matches 14.. if score @s pmVisible matches 1 unless score @s pmWantMode matches 0 run return run function rlk:char/motion/finish
