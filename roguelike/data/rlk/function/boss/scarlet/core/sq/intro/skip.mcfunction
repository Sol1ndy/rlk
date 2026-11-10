# Stand-in skip (the core counted the hold): the black, the rock gone, her E10 end pose <= 7 b from the player
# (on her line to the player, mv/ok), facing them; the core then jumps the clock.
function rlk:boss/scarlet/fx/hud/ovl {g:"black",in:0,hold:20,out:6}
kill @e[tag=rlk_hr_deco_seat_rock]
function rlk:boss/scarlet/core/stop_move
kill @e[type=minecraft:marker,tag=rlk_hr_near]
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^6.5 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_near"]}
scoreboard players set #t4 hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_near,limit=1] at @s run function rlk:boss/scarlet/core/clamp
execute at @s unless entity @e[tag=rlk_body,limit=1,distance=..7] positioned as @e[type=minecraft:marker,tag=rlk_hr_near,limit=1] run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_hr_near]
function rlk:mboss/mv/face
