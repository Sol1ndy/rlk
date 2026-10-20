# Launch (t32): one new volley group; target 0 = lockv (lead 8), 1 / 2 = random 7-14 b from here;
# every target out of the clear melee points; the hazards (tell = the flight); the props fly.
function rlk:mboss/grp_new
function rlk:mboss/mv/lockv {lead:8}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_x
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_xlw
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_xlwt
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_xlwt0
tag @e[type=minecraft:marker,tag=rlk_mb_lock] remove rlk_mb_lock
execute store result storage rlk:mboss az.xl.r.a int 1 run random value 0..359
execute store result storage rlk:mboss az.xl.r.d int 1 run random value 7..14
data modify storage rlk:mboss az.xl.r.t set value "rlk_mb_az_xlwt1"
function rlk:mboss/azhdaha/xl/u/rnd with storage rlk:mboss az.xl.r
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_xlw
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_xlwt
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] remove rlk_mb_az_xnt
execute store result storage rlk:mboss az.xl.r.a int 1 run random value 0..359
execute store result storage rlk:mboss az.xl.r.d int 1 run random value 7..14
data modify storage rlk:mboss az.xl.r.t set value "rlk_mb_az_xlwt2"
function rlk:mboss/azhdaha/xl/u/rnd with storage rlk:mboss az.xl.r
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_xlw
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_xlwt
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] remove rlk_mb_az_xnt
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xlwt] run function rlk:mboss/azhdaha/xl/u/clear_lump
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xlwt] at @s run function rlk:mboss/azhdaha/xl/u/lump_hz
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xlwp0,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_xlwt0,limit=1] run function rlk:mboss/azhdaha/xl/u/lump_fly
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xlwp1,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_xlwt1,limit=1] run function rlk:mboss/azhdaha/xl/u/lump_fly
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xlwp2,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_xlwt2,limit=1] run function rlk:mboss/azhdaha/xl/u/lump_fly
playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.7 0.6 0.23
scoreboard players set #azAftF mb 6
scoreboard players set #azAftD mb 13
function rlk:mboss/azhdaha/aft/new
scoreboard players set #azAftF mb 7
scoreboard players set #azAftD mb 26
function rlk:mboss/azhdaha/aft/new
