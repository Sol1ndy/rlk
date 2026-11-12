# @s = the chapter zone marker, at it (from room/combat_clear: the body is gone, #combat 0). Killed: the next-chapter
# object (room/obj/k_chapter); cancelled: cb/won put the gate back.
execute store result score #cbW mb run function rlk:mboss/cb/won
execute if score #cbW mb matches 1 run function rlk:room/obj/k_chapter
