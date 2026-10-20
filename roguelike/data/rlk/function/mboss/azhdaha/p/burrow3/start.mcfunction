# 23 the B3 frame (WORKING STUB, S1-MOD; s2.md 7): #azB3T = #azPT; dig, inv 8, the hidden glide to the
# centre (40, 56), tail-up 58 (tail_only, #azBur 1, the special starts), sink 335, emergence
# decal 360, burst 388 (the special stops), out 418 (normal, floor 0), end 433.
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/azhdaha/kstub/tele/crater
execute if score #azE mb matches 1 run function rlk:mboss/azhdaha/kstub/p/dig/1
execute if score #azE mb matches 2 run function rlk:mboss/azhdaha/kstub/p/dig/2
execute if score #azE mb matches 3 run function rlk:mboss/azhdaha/kstub/p/dig/3
execute if score #azE mb matches 4 run function rlk:mboss/azhdaha/kstub/p/dig/4
execute if score #azE mb matches 5 run function rlk:mboss/azhdaha/kstub/p/dig/5
function rlk:mboss/azhdaha/kstub/snd/b3_sink
scoreboard players set #mbNoLeash mb 1
scoreboard players set #azB3Sp mb 0
