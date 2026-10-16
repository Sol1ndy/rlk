function rlk:char/motion/audio/navia/skill
# Skill tap (owner: skill), started by char/navia/tap (the charge is already spent). Locked until the shot;
# the shot itself (pellets, damage, Geo passive, muzzle fx and blast sound, first-person gun) is char/navia/fire.
# This clip keeps its starting heading (the parasol is left standing in the world at 25-27). The heading is the
# avatar's facing when the skill was pressed ("basis":"body": view/face_lock has just turned it toward the crosshair
# point), so char/navia/fire_dir fires along it with the avatar's pitch: the shot converges on the crosshair and
# turning the camera never sends it out sideways.
execute if score @s pmTick matches 0 run scoreboard players set @s pmLockUntil 7
execute if score @s pmTick matches 0 run function rlk:char/motion/control/lock
execute if score @s pmTick matches 7 if score @s nvShot matches 1.. run function rlk:char/navia/fire_dir
# Moving (or leaving the ground) during the recovery: the parasol sparkles away, the halberd re-forms on the back
# and sheathed locomotion takes over (same quick stow as an interrupted put-away), instead of sliding the kneel.
execute if score @s pmTick matches 9.. if score @s pmVisible matches 1 unless score @s pmWantMode matches 0 run return run function rlk:char/motion/sheath/abort
