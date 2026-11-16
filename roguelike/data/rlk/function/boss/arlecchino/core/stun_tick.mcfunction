# Stun tick (#pat 50, @s = body): the stun clip after the stagger, motes, the countdown.
scoreboard players add #pt kn 1
scoreboard players remove #stun_t kn 1
execute if score #pt kn matches 20 run function rlk:boss/arlecchino/core/stun_clip
execute if score #pt kn matches 20.. if score #stun_t kn matches 1.. run function rlk:boss/arlecchino/core/stun_fx
execute if score #stun_t kn matches ..0 run function rlk:boss/arlecchino/core/stun_end
