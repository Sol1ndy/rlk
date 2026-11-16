# Launch (t49): one new volley group; target 0 = lockv (lead 8), 1 / 2 = random 7-14 b from here;
# every target out of the clear melee points; the hazards (tell = the flight); the props fly.
function rlk:mboss/grp_new
scoreboard players operation #axlLG mb = #mbGrp mb
function rlk:mboss/mv/lockv {lead:8}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_x
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_xls
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_xlst
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_xlst0
tag @e[type=minecraft:marker,tag=rlk_mb_lock] remove rlk_mb_lock
execute store result storage rlk:mboss az.xl.r.a int 1 run random value 0..359
execute store result storage rlk:mboss az.xl.r.d int 1 run random value 7..14
data modify storage rlk:mboss az.xl.r.t set value "rlk_mb_az_xlst1"
function rlk:boss/azhdaha/xl/u/rnd with storage rlk:mboss az.xl.r
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_xls
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_xlst
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] remove rlk_mb_az_xnt
execute store result storage rlk:mboss az.xl.r.a int 1 run random value 0..359
execute store result storage rlk:mboss az.xl.r.d int 1 run random value 7..14
data modify storage rlk:mboss az.xl.r.t set value "rlk_mb_az_xlst2"
function rlk:boss/azhdaha/xl/u/rnd with storage rlk:mboss az.xl.r
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_xls
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] add rlk_mb_az_xlst
tag @e[type=minecraft:marker,tag=rlk_mb_az_xnt] remove rlk_mb_az_xnt
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xlst] run function rlk:boss/azhdaha/xl/u/clear_lump
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xlst0,limit=1] at @s run function rlk:boss/azhdaha/xl/u/lump_hz0
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_xlsp0,limit=1] at @e[type=minecraft:marker,tag=rlk_mb_az_xlst0,limit=1] run function rlk:boss/azhdaha/xl/u/lump_fly0
playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.7 0.6 0.23
scoreboard players set #azAftF mb 17
scoreboard players set #azAftD mb 1
function rlk:boss/azhdaha/aft/new
