$execute unless data storage rlk:mboss sbyid.$(id) run return run tellraw @s [{text:"[균열] ",color:"#7FD8FF",bold:true},{text:"등록되지 않았거나 꺼진 특수 보스입니다: $(id)",color:"gray",bold:false}]
$data modify storage rlk:mboss spforce set value {id:"$(id)"}
scoreboard players set #riftForce room 1
$tellraw @s [{text:"[균열] ",color:"#7FD8FF",bold:true},{text:"다음에 여는 방에 균열이 나타납니다: ",color:"gray",bold:false},{nbt:"sbyid.$(id).name",storage:"rlk:mboss",color:"#FFE08A",bold:false},{text:" (보스 · 중간보스 방 제외)",color:"gray",bold:false}]
