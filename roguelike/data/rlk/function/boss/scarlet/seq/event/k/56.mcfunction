# event: the timeline at #sq 56 (@s = the body).
kill @e[type=minecraft:item_display,tag=rlk_hr_ev_sword]
function rlk:boss/scarlet/ev/apply
function rlk:boss/scarlet/ev/title
execute if score #hrEv hr matches 1 at @e[tag=rlk_body,limit=1] positioned ~ ~1.1 ~ run function rlk:boss/scarlet/fx/p/ev_take {c:1}
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/fx/snd/ev_take_i
execute if score #hrEv hr matches 2 at @e[tag=rlk_body,limit=1] positioned ~ ~1.1 ~ run function rlk:boss/scarlet/fx/p/ev_take {c:2}
execute if score #hrEv hr matches 2 run function rlk:boss/scarlet/fx/snd/ev_take_b
execute at @e[tag=rlk_body,limit=1] positioned ~ ~0.8 ~ run function rlk:boss/scarlet/fx/p/ev_petals {n:2}
