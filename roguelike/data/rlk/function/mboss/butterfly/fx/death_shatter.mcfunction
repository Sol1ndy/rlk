# The wings shatter into lime / opal shards.
particle minecraft:block{block_state:"minecraft:lime_stained_glass"} ~ ~3.0 ~ 1.8 1 0.6 0 30 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:white_stained_glass"} ~ ~3.0 ~ 1.6 1 0.6 0 16 force @a[tag=player]
particle minecraft:dust{color:[0.831f,0.973f,0.776f],scale:1.4} ~ ~3.0 ~ 2 1.2 0.8 0 20 force @a[tag=player]
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
execute positioned ^ ^3.0 ^ rotated ~0 -35 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.8,s1:1.8,move:"0f,0f,0f",life:12,fade:6,col:11985754,ax:"0f,0f,1f"}
execute positioned ^ ^3.0 ^ rotated ~60 -15 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.8,s1:1.8,move:"0f,0f,0f",life:12,fade:6,col:13957318,ax:"0f,0f,1f"}
execute positioned ^ ^3.0 ^ rotated ~120 5 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.8,s1:1.8,move:"0f,0f,0f",life:12,fade:6,col:9300720,ax:"0f,0f,1f"}
execute positioned ^ ^3.0 ^ rotated ~180 -35 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.8,s1:1.8,move:"0f,0f,0f",life:12,fade:6,col:11985754,ax:"0f,0f,1f"}
execute positioned ^ ^3.0 ^ rotated ~240 -15 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.8,s1:1.8,move:"0f,0f,0f",life:12,fade:6,col:13957318,ax:"0f,0f,1f"}
execute positioned ^ ^3.0 ^ rotated ~300 5 run function rlk:mboss/butterfly/tc/card {kind:"shard",bb:"fixed",roll:0,spin:0,s0:0.8,s1:1.8,move:"0f,0f,0f",life:12,fade:6,col:9300720,ax:"0f,0f,1f"}
