# Nothing of its own lingers (dust only). A cut in the fight (test commands; #mbSt 1) after the open event
# (3) put the rig in butterfly form while #bfForm is still 1: back to the human rig (review fix S3).
# A death keeps the wings so they can shatter; a reload respawns the rig anyway.
execute if score #mbSt mb matches 1 if score #bfForm mb matches 1 if score #bfPT mb matches 3.. as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/butterfly/form/rig_h
