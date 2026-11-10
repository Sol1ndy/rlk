# lead_re: the timeline at #sq 10 (@s = the body).
function rlk:boss/scarlet/rig/face/track
scoreboard players set #sq_sig hr 4
function rlk:boss/scarlet/fx/snd/shield_refill
execute if score #warn hr matches 1 run function rlk:boss/scarlet/fx/hud/warn {on:1}
execute positioned ~ ~1.1 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/shield_refill
