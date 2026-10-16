function rlk:char/motion/audio/navia/skill_fire
# Skill hold release (owner: skill), started by char/navia/aim_release (charge spent). Locked until the blast.
# The rig turns with the look every tick here, so char/navia/fire_dir fires along the look.
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 3
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 3 if score @s nvShot matches 1.. run function rlk:char/navia/fire_dir
# Moving (or leaving the ground) during the recovery: quick stow into sheathed locomotion instead of sliding the squat.
execute if score @s pmTick matches 5.. if score @s pmVisible matches 1 unless score @s pmWantMode matches 0 run return run function rlk:char/motion/sheath/abort
