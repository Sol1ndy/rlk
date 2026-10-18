# @s = body: the wing element look #bfWant (1 pyro: orange-gold with magenta rims, 7 dendro: lime/opal), a 1 t
# swap with a flash of its colour.
scoreboard players operation #bfLook mb = #bfWant mb
execute if score #bfLook mb matches 1 run function rlk:mboss/butterfly/rig_stub/look/pyro
execute if score #bfLook mb matches 7 run function rlk:mboss/butterfly/rig_stub/look/dendro
execute if score #bfLook mb matches 1 run particle minecraft:dust_color_transition{from_color:[0.98f,0.843f,0.486f],to_color:[0.776f,0.502f,0.635f],scale:1.4} ~ ~3.0 ~ 1.6 1 0.6 0 24 force @a[tag=player]
execute if score #bfLook mb matches 1 run particle minecraft:flame ~ ~3.0 ~ 1.4 0.8 0.5 0.02 10 force @a[tag=player]
execute if score #bfLook mb matches 1 run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
execute if score #bfLook mb matches 7 run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.3} ~ ~3.0 ~ 1.6 1 0.6 0 24 force @a[tag=player]
execute if score #bfLook mb matches 7 run playsound minecraft:block.azalea_leaves.break hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute if score #bfLook mb matches 1 run execute positioned ^ ^3.0 ^ rotated ~ ~ run function rlk:mboss/butterfly/tc/card {kind:"glow",bb:"center",roll:0,spin:0,s0:1.5,s1:5,move:"0f,0f,0f",life:6,fade:3,col:16439164,ax:"0f,0f,1f"}
execute if score #bfLook mb matches 7 run execute positioned ^ ^3.0 ^ rotated ~ ~ run function rlk:mboss/butterfly/tc/card {kind:"glow",bb:"center",roll:0,spin:0,s0:1.5,s1:5,move:"0f,0f,0f",life:6,fade:3,col:11985754,ax:"0f,0f,1f"}
function rlk:mboss/butterfly/hud/refresh
