# The cutscene actor. @s = the player, at the stage marker, rotated as the stage (hr_design.md §5.3). The root and the 11
# displays in the avatar's idle pose with the current character's skin and the one sword; the avatar (and a rig character's own
# displays, a floating catalyst) hidden. Called again it only moves the actor to the new stage.
scoreboard objectives add cine dummy
execute store result score #n cine if entity @e[type=minecraft:item_display,tag=rlk_cine_part]
execute if score #n cine matches 11 if entity @e[type=minecraft:marker,tag=rlk_cine_root,limit=1] if score #cavCh cine = #charN tmp run return run function rlk:char/cine/place
function rlk:char/cine/clear
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_cine_root"]}
data modify storage rlk:cine sp set value {k:"lumine"}
execute if score #charN tmp matches 3 run data modify storage rlk:cine sp.k set value "skirk"
execute if score #charN tmp matches 4 run data modify storage rlk:cine sp.k set value "clorinde"
execute if score #charN tmp matches 5 run data modify storage rlk:cine sp.k set value "arle"
execute if score #charN tmp matches 6 run data modify storage rlk:cine sp.k set value "navia"
execute if score #charN tmp matches 7 run data modify storage rlk:cine sp.k set value "ronova"
execute if score #charN tmp matches 8 run data modify storage rlk:cine sp.k set value "nefer"
function rlk:char/cine/parts with storage rlk:cine sp
scoreboard players operation #cavCh cine = #charN tmp
scoreboard players set #cavP cine -99
scoreboard players set #cavR cine -1
scoreboard players set #cavF cine 0
function rlk:char/cine/place
