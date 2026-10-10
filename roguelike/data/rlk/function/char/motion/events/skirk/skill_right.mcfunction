function rlk:char/motion/audio/skirk/skill_right
execute if score @s pmTick matches 17 if score @s skDash matches 1.. run function rlk:char/motion/start {char:"skirk",clip:"skill_right_loop"}
