# Generated: the put-away clip (clips.sheathe) when the character has one, else a quick stow.
execute if score #charN tmp matches 5 run return run function rlk:char/motion/start {char:"arle",clip:"sheathe"}
function rlk:char/motion/sheath/stow
