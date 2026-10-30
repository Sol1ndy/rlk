$execute if entity @e[tag=rlk_pm] run function rlk:char/motion/clips/$(char)/$(clip)/pose
function rlk:char/motion/sheath/clip_state
execute store result score #pmFxFP tmp unless score @s pmVisible matches 1
$function rlk:char/motion/$(char)_fx/$(clip)
scoreboard players set #pmFxFP tmp 0
function rlk:char/motion/event
