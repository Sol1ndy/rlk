function rlk:char/motion/audio/navia/physical_3
# Normal attack 3 (owner: na3): drag, plant, kick; the thrown halberd cartwheels at the target and dissolves, then
# re-forms on her back (weapon_attach world 8-25, back from 26; retimed to playback 100, 38 ticks). Three timeline
# hits from the generated combat/config/navia/physical_3: pmStrike/pmSecond/pmThird = hit_ticks 14/16/18 ->
# combat/first (find_immediate, queues the 94% extras), combat/second and combat/third (char/melee/extra each).
# Retime (Genshin recovery): kick 11, hits 14/16/18, chain 19, halberd back 26, IDLE_S 38.
scoreboard players set @s cboIdle 0
# Moving or jumping from the chain tick on: quick stow (the thrown halberd or its re-form goes to the back) and sheathed locomotion.
execute if score @s pmTick matches 19.. if score @s pmVisible matches 1 unless score @s pmWantMode matches 0 run return run function rlk:char/motion/sheath/abort
