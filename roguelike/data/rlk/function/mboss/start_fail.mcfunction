# Spawn failed (no registry entry, unloaded arena, peaceful): retry twice, then cancel without reward.
function rlk:mboss/cleanup_aux
scoreboard players add #mbFail mb 1
execute if score #mbFail mb matches ..2 run return run scoreboard players set #spawnT room 10
scoreboard players set #mbFail mb 0
scoreboard players set #mbKilled mb 0
tellraw @a[tag=player] [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"중간보스를 불러오지 못해 전투를 취소했습니다. (보상 없음)",color:"gray",bold:false}]
function rlk:room/combat_clear
