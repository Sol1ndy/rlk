function rlk:player/bol/pct
scoreboard players operation #bolPct tmp = #arAbsMax tmp
scoreboard players operation #bolPct tmp -= #bolNow tmp
execute if score #bolPct tmp > #arAbs tmp run scoreboard players operation #bolPct tmp = #arAbs tmp
execute if score #bolPct tmp matches ..0 run return 0
function rlk:player/bol/add_pct
playsound minecraft:block.respawn_anchor.charge master @s ~ ~ ~ 0.6 0.8
