summon minecraft:mannequin 8.5 120 0.5 {UUID:[I;1,2,3,4],Tags:["rvpA","rlk_cb_fx","rlk_cb_ghost","rlk_pet"],hide_description:1b,immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,Glowing:1b,active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}]}
team join rlk_cbred @e[tag=rvpA]
execute store result score @e[tag=rvpA] cb run scoreboard players get #cb0 rvp
scoreboard players set #mode rvp 1
