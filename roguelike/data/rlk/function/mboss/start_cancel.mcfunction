# @s = zone marker: give up this attempt (no reward); room/combat_clear -> mboss/won brings the gate back.
scoreboard players set #mbFail mb 0
scoreboard players set #mbLd mb 0
scoreboard players set #mbKilled mb 0
tellraw @a[tag=player] [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"중간보스를 불러오지 못해 전투를 취소했습니다. (보상 없음)",color:"gray",bold:false}]
function rlk:room/combat_clear
