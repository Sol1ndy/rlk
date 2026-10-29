# @s = zone marker: give up this attempt (no reward); room/combat_clear -> mboss/won (chapter: cb/clear -> cb/won)
# brings the gate back.
scoreboard players set #mbFail mb 0
scoreboard players set #mbLd mb 0
scoreboard players set #mbKilled mb 0
scoreboard players set #cbWait mb 0
execute unless data storage rlk:mboss cur{kind:"chapter"} unless score #spOn mb matches 1 run tellraw @a[tag=player] [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"중간보스를 불러오지 못해 전투를 취소했습니다. (보상 없음)",color:"gray",bold:false}]
execute if data storage rlk:mboss cur{kind:"chapter"} run tellraw @a[tag=player] [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"보스를 불러오지 못해 전투를 취소했습니다. (보상 없음)",color:"gray",bold:false}]
execute if score #spOn mb matches 1 run tellraw @a[tag=player] [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"특수 보스를 불러오지 못해 전투를 취소했습니다. (보상 없음)",color:"gray",bold:false}]
function rlk:room/combat_clear
