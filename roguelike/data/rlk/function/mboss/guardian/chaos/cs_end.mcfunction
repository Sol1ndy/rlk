# @s = a lead that landed: it bursts and turns invisible; the followers pop into its place one per tick.
tag @s add rlk_mb_gd_csend
data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,0f,0f],scale:[0f,0f,0f]}}
particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~ ~ 0.2 0.2 0.2 0 6 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~ ~ 0.25 0.2 0.25 0 6 force @a[tag=player]
playsound minecraft:block.chain.place hostile @a[tag=player] ~ ~ ~ 0.3 1.4 0.1
