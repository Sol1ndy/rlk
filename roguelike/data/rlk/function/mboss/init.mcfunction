# From rlk:load. Objectives, the three boss bars, registry, tables; a /reload keeps a running fight
# (HP kept, aux entities rebuilt by the module reload hook).
scoreboard objectives add mb dummy
scoreboard objectives add mres dummy
scoreboard objectives add pkMb dummy
scoreboard objectives add mbHzK dummy
scoreboard objectives add mbHzT dummy
scoreboard objectives add mbHzW dummy
scoreboard objectives add mbHzA dummy
scoreboard objectives add mbHzL dummy
scoreboard objectives add mbHzD dummy
scoreboard objectives add mbHzE dummy
scoreboard objectives add mbHzB dummy
scoreboard objectives add mbHzKD dummy
scoreboard objectives add mbHzS dummy
scoreboard objectives add mbHzV dummy
scoreboard objectives add mbHzI dummy
scoreboard objectives add mbHzR dummy
scoreboard objectives add mbHzR0 dummy
scoreboard objectives add mbHzC dummy
scoreboard objectives add mbHzAng dummy
scoreboard objectives add mbHzRR dummy
scoreboard objectives add mbHzRI dummy
scoreboard objectives add mbHzLo dummy
scoreboard objectives add mbHzHi dummy
scoreboard objectives add mbHzHW dummy
scoreboard objectives add mbHzFX dummy
scoreboard objectives add mbHzFZ dummy
scoreboard objectives add mbHzY0 dummy
scoreboard objectives add mbHzY1 dummy
scoreboard objectives add mbHzHit dummy
scoreboard objectives add mbHzCol dummy
scoreboard objectives add mbHzG dummy
scoreboard objectives add mbHzND dummy
scoreboard objectives add mbHzRA dummy
scoreboard objectives add mbHzRT dummy
scoreboard objectives add mbPjV dummy
scoreboard objectives add mbPjT dummy
scoreboard objectives add mbPjL dummy
scoreboard objectives add mbPjD dummy
scoreboard objectives add mbPjE dummy
scoreboard objectives add mbPjB dummy
scoreboard objectives add mbPjR dummy
scoreboard objectives add mbPjHit dummy
scoreboard objectives add mbPjRet dummy
scoreboard objectives add mbPjW dummy
scoreboard objectives add mbPjK dummy
scoreboard objectives add mbPjG dummy
scoreboard objectives add mbPlT dummy
scoreboard objectives add mbPlF dummy
scoreboard objectives add mbMvK dummy
scoreboard objectives add mbMvT dummy
scoreboard objectives add mbMvN dummy
scoreboard objectives add mbMvH dummy
scoreboard objectives add mbMvX0 dummy
scoreboard objectives add mbMvY0 dummy
scoreboard objectives add mbMvZ0 dummy
scoreboard objectives add mbMvX1 dummy
scoreboard objectives add mbMvY1 dummy
scoreboard objectives add mbMvZ1 dummy
scoreboard objectives add mbT dummy
scoreboard objectives add mbS dummy
scoreboard objectives add mbId dummy
bossbar add rlk:mboss {text:"중간보스"}
bossbar add rlk:mboss_state {text:""}
bossbar add rlk:mboss_sub {text:""}
# Resource-pack boss bar (tools/build_bossbar.py): white bars are transparent; the names carry
# the name line, the drawn HP bar (bossui) and the module sub-line.
bossbar set rlk:mboss color white
bossbar set rlk:mboss_state color white
bossbar set rlk:mboss_sub color white
bossbar set rlk:mboss style progress
bossbar set rlk:mboss_state style progress
bossbar set rlk:mboss_sub style progress
function rlk:mboss/register
data modify storage rlk:mboss cos set value [1000,1000,999,999,998,996,995,993,990,988,985,982,978,974,970,966,961,956,951,946,940,934,927,921,914,906,899,891,883,875,866,857,848,839,829,819,809,799,788,777,766,755,743,731,719,707,695,682,669,656,643,629,616,602,588,574,559,545,530,515,500,485,469,454,438,423,407,391,375,358,342,326,309,292,276,259,242,225,208,191,174,156,139,122,105,87,70,52,35,17,0,-17,-35,-52,-70,-87,-105,-122,-139,-156,-174,-191,-208,-225,-242,-259,-276,-292,-309,-326,-342,-358,-375,-391,-407,-423,-438,-454,-469,-485,-500,-515,-530,-545,-559,-574,-588,-602,-616,-629,-643,-656,-669,-682,-695,-707,-719,-731,-743,-755,-766,-777,-788,-799,-809,-819,-829,-839,-848,-857,-866,-875,-883,-891,-899,-906,-914,-921,-927,-934,-940,-946,-951,-956,-961,-966,-970,-974,-978,-982,-985,-988,-990,-993,-995,-996,-998,-999,-999,-1000,-1000]
# Telegraph colours by #elem 0..8, then 9 = strike flash, 10 = safe zone.
data modify storage rlk:mboss hzc set value ["[0.86f,0.16f,0.18f]","[1f,0.38f,0.1f]","[0.18f,0.55f,1f]","[0.7f,0.3f,1f]","[0.3f,0.82f,0.95f]","[0.9f,0.52f,0.06f]","[0.25f,0.85f,0.7f]","[0.45f,0.8f,0.15f]","[0.85f,0.15f,0.4f]","[1f,0.97f,0.88f]","[0.35f,0.95f,0.45f]"]
execute unless data storage rlk:mboss met run data modify storage rlk:mboss met set value []
execute unless data storage rlk:mboss sub run data modify storage rlk:mboss sub set value []
execute unless data storage rlk:mboss extra run data modify storage rlk:mboss extra set value []
execute unless data storage rlk:mboss aura run data modify storage rlk:mboss aura set value []
scoreboard players set #c2 mb 2
scoreboard players set #c4 mb 4
scoreboard players set #c10 mb 10
scoreboard players set #c30 mb 30
scoreboard players set #c100 mb 100
scoreboard players set #c500 mb 500
scoreboard players set #c1000 mb 1000
scoreboard players set #c10000 mb 10000
scoreboard players set #cm1 mb -1
scoreboard players set #c36000 mb 36000
execute unless score #mbOn mb matches 0.. run scoreboard players set #mbOn mb 0
execute unless score #mbSt mb matches 0.. run scoreboard players set #mbSt mb 0
execute unless score #mbKilled mb matches 0.. run scoreboard players set #mbKilled mb 0
execute unless score #mbTest mb matches 0.. run scoreboard players set #mbTest mb 0
execute unless score #mbForce mb matches 0.. run scoreboard players set #mbForce mb 0
execute unless score #mbLock mb matches 0.. run scoreboard players set #mbLock mb 0
execute unless score #mbId mb matches 0.. run scoreboard players set #mbId mb 0
execute unless score #mbGoldMul mb matches 1.. run scoreboard players set #mbGoldMul mb 5
execute unless score #mbSap mb matches 0.. run scoreboard players set #mbSap mb 1
execute unless score #mbLive mb matches 0.. run scoreboard players set #mbLive mb 0
execute unless score #mbLd mb matches 0.. run scoreboard players set #mbLd mb 0
# Player-side fight modifiers a module may set (player_heal, items/hook/stat_buffs); a /reload keeps a
# running fight's values (the module reload hook re-asserts them), so only unset ones are initialised.
execute unless score #mbHealPct mb matches -1000.. run scoreboard players set #mbHealPct mb 100
execute unless score #mbCritAdd mb matches -1000.. run scoreboard players set #mbCritAdd mb 0
execute unless score #mbHealEv mb matches 0.. run scoreboard players set #mbHealEv mb 0
execute unless score #mbGrpN mb matches 0.. run scoreboard players set #mbGrpN mb 0
# Low gravity requested by the running module (#mbLowG 1; mboss/main clears it every tick, the module tick sets it
# again; rlk:tick syncs the attribute modifiers through mboss/lowg_on|off). Hazard re-arm clock (hz/all).
execute unless score #mbLowG mb matches 0..1 run scoreboard players set #mbLowG mb 0
execute unless score #mbHzClk mb matches 0.. run scoreboard players set #mbHzClk mb 0
scoreboard players set #mbNoDodge mb 0
# Library activity flags (a set flag makes the world tick scan for that library's entities once).
scoreboard players set #mbHzOn mb 1
scoreboard players set #mbPjOn mb 1
scoreboard players set #mbPlOn mb 1
scoreboard players set #mbMvOn mb 1
function rlk:mboss/opts_reset
function rlk:mboss/bars_hide
scoreboard players set #mbLn mb 0
# Every helper entity dies on reload; a surviving body rebuilds its own (module reload hook).
kill @e[tag=rlk_mb_aux]
execute as @e[tag=rlk_mb_body] at @s run function rlk:mboss/reload
# The arena is built once the dungeon area is set up (room/setup) and its chunks are loaded.
execute if data storage rlk:room {ready:1b} in minecraft:overworld if loaded 200 201 8 run function rlk:mboss/arena/ensure
