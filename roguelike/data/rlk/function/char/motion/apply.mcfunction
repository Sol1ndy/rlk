$execute if entity @e[tag=rlk_pm] run function rlk:char/motion/clips/$(char)/$(clip)/pose
function rlk:char/motion/sheath/clip_state
$function rlk:char/motion/$(char)_fx/$(clip)
function rlk:char/motion/event
