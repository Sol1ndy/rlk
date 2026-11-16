# The rift of spproto was entered (@s = its anchor, at it; its zone tagged rlk_spz). While an arena job runs (a build, a look
# restore, the chunks being verified, or another arena's job: #mbArBuild >= 1) the entry is refused (sp/busy). Else the
# forceload comes back (a cancelled fight released it; the chunks load during the 30-t delay), ensure starts whatever job
# the arena still needs (sp/start waits for it, as cb/start), the zone fight starts (doors lock), #spOn 1 (room/mob_wave ->
# sp/start_zone 1.5 s later), the title, and the rift pulls the player in (room/rift/go: state entering, blindness at 20 t).
# Returns 1.
execute if score #mbArBuild mb matches 1.. run return run function rlk:mboss/sp/busy
execute in minecraft:overworld run function rlk:mboss/ar/cp_test/fl_on
execute in minecraft:overworld run function rlk:mboss/ar/cp_test/ensure
scoreboard players set #spOn mb 1
scoreboard players set #spAuto mb 0
scoreboard players set #cbWait mb 0
execute as @e[type=minecraft:marker,tag=rlk_spz,limit=1] at @s run function rlk:room/combat_start
tag @e[tag=rlk_spz] remove rlk_spz
scoreboard players set #spawnT room 30
title @a[tag=player] times 6 46 14
title @a[tag=player] subtitle {text:"특수 보스 틀 점검용",color:"#E8E2D0"}
title @a[tag=player] title {text:"시험용 균열 수호자",color:"#8FD8FF",bold:true}
scoreboard players set @a[tag=player] vBig 66
scoreboard players set @a[tag=player] ttlT 66
execute as @a[tag=player] at @s run playsound minecraft:block.bell.resonate hostile @s ~ ~ ~ 0.7 0.6
execute as @a[tag=player] at @s run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 0.7
function rlk:room/rift/go
return 1
