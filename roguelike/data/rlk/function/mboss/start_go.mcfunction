# The shared start body (@s = the zone marker, at @s; cur is set): mboss/start (mid-boss, plaza) and mboss/cb/start
# (chapter boss, its own arena, already built: arena ensure reported 1). fight_vars sets #mbMode and #mbAr from cur.
scoreboard players set #mbLd mb 0
# From here on fight entities may exist: rlk:tick runs mboss/main (cleared when the body is gone).
scoreboard players set #mbLive mb 1
function rlk:mboss/cleanup_aux
function rlk:mboss/fight_vars
execute if score #mbMode mb matches 0 in minecraft:overworld run function rlk:mboss/arena/ensure
execute in minecraft:overworld run function rlk:mboss/ar/marker
execute in minecraft:overworld as @e[tag=rlk_mb_arena,limit=1] at @s rotated as @s run function rlk:mboss/d/spawn
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run function rlk:mboss/start_fail
scoreboard players set #mbFail mb 0
scoreboard players set #cbWait mb 0
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/start_body
function rlk:mboss/ret_save
scoreboard players operation #mbLv mb = @e[tag=rlk_mb_body,limit=1] mlv
execute if score #mbMode mb matches 0 run data modify storage rlk:mboss met append from storage rlk:mboss cur.id
scoreboard players set #mbOn mb 1
scoreboard players set #mbSt mb 0
scoreboard players set #mbT mb 0
execute as @a[tag=player,limit=1] run function rlk:mboss/tp_in
function rlk:mboss/bars_show
