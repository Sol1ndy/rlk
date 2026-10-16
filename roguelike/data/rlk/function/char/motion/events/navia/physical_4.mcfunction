function rlk:char/motion/audio/navia/physical_4
# Normal attack 4 (owner: na4; retimed to playback 100, 62 ticks). Damage: generated combat/config/navia/physical_4 (pmStrike = hit_ticks[0]).
# Retime (Genshin recovery): shot 12, take-off 14-15, apex 19, canopy open 21-35 (15 ticks; float 21-28), landing 28 =
# chain 28, parasol gone + halberd on the back 43, IDLE_S 62.
# Keep the string alive while the tail plays (player/tick resets comboStep after 20 idle ticks).
scoreboard players set @s cboIdle 0
# Moving or jumping after the landing, once a chained click would be accepted (#pmChainOpen, see physical_1): the
# parasol sparkles away, the halberd goes to the back, sheathed locomotion.
execute if score @s pmTick matches 28.. if score #pmChainOpen tmp matches 1 if score @s pmVisible matches 1 unless score @s pmWantMode matches 0 run return run function rlk:char/motion/sheath/abort
