# Positions taken: everyone turns to the centre, settles into the guard, can be hit.
execute as @e[tag=rlk_rd_illusion] at @s facing entity @e[tag=rlk_raiden_arena,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set @e[tag=rlk_rd_illusion] rdHitCD 0
execute as @e[type=minecraft:item_display,tag=rlk_rd_ilvis] run data merge entity @s {interpolation_duration:3,start_interpolation:0,transformation:{translation:[0.000000f,1.200000f,0.000000f],left_rotation:[0.000000f,0.000000f,0.000000f,1.000000f],scale:[2.400000f,2.400000f,2.400000f],right_rotation:[0f,0f,0f,1f]}}
function rlk:boss/raiden/illusion/frame {model:"illusion_ready"}
playsound minecraft:entity.breeze.land hostile @a[tag=player] ~ ~ ~ 0.8 1.3 0.2
scoreboard players set #rdIlStep rd 2
# Turns start next tick (clock 1).
scoreboard players set #rdIlClock rd -1
