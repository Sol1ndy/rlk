# @s = an opened box's object marker, at @s (box centre): the open fx (chest opening, chime, gold burst, poof), then
# the whole group (marker, chest display, label, hint) via room/obj/kill_group. From box/spend, and from
# room/obj/do_mbox for an opened box whose pick no longer exists (guard only: pkMb < 1 with an opened box).
# The two sounds play at the player: a pick is used in the selection screen (overworld 104 195 4), at least 40 b
# from any box in the room (-64..63), where a sound at the box (heard up to 16 b) would never reach the player.
execute at @a[tag=player,limit=1] run playsound minecraft:block.chest.open block @a[tag=player] ~ ~ ~ 0.9 1
execute at @a[tag=player,limit=1] run playsound minecraft:block.amethyst_block.chime block @a[tag=player] ~ ~ ~ 1 1.2
particle minecraft:dust{color:[1.0f,0.84f,0.36f],scale:1.4f} ~ ~ ~ 0.35 0.35 0.35 0 18
particle minecraft:end_rod ~ ~0.2 ~ 0.15 0.15 0.15 0.1 12
particle minecraft:poof ~ ~-0.45 ~ 0.35 0.25 0.35 0.02 12
function rlk:room/obj/kill_group
