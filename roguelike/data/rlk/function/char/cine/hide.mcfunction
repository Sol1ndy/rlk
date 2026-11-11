# Internal, every tick while the actor stands: the avatar invisible with empty hands (1 s at a time: it shows again by
# itself if the ticks stop), a rig character's displays and a floating catalyst out of view range until stop.
# Round V (lane VC): the player watches a locked sequence as a spectator, and a spectator sees an invisible living
# entity as a 15 % ghost drawn with its own texture: the avatar's skin is the blank one until stop (blank / show).
execute as @e[tag=rlk_av,tag=!rlk_cine_hid,limit=1] run function rlk:char/cine/blank
effect give @e[tag=rlk_av,limit=1] minecraft:invisibility 1 0 true
item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air
item replace entity @e[tag=rlk_av,limit=1] weapon.offhand with minecraft:air
tag @e[tag=rlk_av,limit=1] add rlk_cine_hid
execute as @e[type=minecraft:item_display,tag=rlk_pm,tag=!rlk_cine_hid] run function rlk:char/cine/hide_one
execute as @e[type=minecraft:block_display,tag=rlk_rncat,tag=!rlk_cine_hid] run function rlk:char/cine/hide_one
execute as @e[type=minecraft:block_display,tag=rlk_nfcat,tag=!rlk_cine_hid] run function rlk:char/cine/hide_one
