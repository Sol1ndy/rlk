# The boss-bar sub line (@s any; on every state change): phase title + the running pattern name (names only).
data modify storage rlk:mboss sub set value []
execute if score #ph tk matches 1 run data modify storage rlk:mboss sub set value [{text:"망토",color:"#F2C230",bold:true}]
execute if score #ph tk matches 2 run data modify storage rlk:mboss sub set value [{text:"과부하 외피",color:"#FFD86B",bold:true}]
execute if score #ph tk matches 3 run data modify storage rlk:mboss sub set value [{text:"날개 전개",color:"#F2C230",bold:true}]
execute if score #ph tk matches 4 run data modify storage rlk:mboss sub set value [{text:"날개",color:"#F2C230",bold:true}]
execute if score #ph tk matches 5 run data modify storage rlk:mboss sub set value [{text:"과부하 외피",color:"#FFD86B",bold:true}]
execute if score #ph tk matches 6 run data modify storage rlk:mboss sub set value [{text:"심연",color:"#E0365F",bold:true}]
execute if score #ph tk matches 7 run data modify storage rlk:mboss sub set value [{text:"심연",color:"#E0365F",bold:true}]
execute if score #pat tk matches 1 run data modify storage rlk:mboss sub append value {text:"  ·  돌진 베기",color:"#E8E2D0",bold:false}
execute if score #pat tk matches 2 run data modify storage rlk:mboss sub append value {text:"  ·  날개 가리기 2연격",color:"#E8E2D0",bold:false}
execute if score #pat tk matches 3 run data modify storage rlk:mboss sub append value {text:"  ·  옆걸음 4연격",color:"#E8E2D0",bold:false}
execute if score #pat tk matches 4 run data modify storage rlk:mboss sub append value {text:"  ·  충전 6연격",color:"#E8E2D0",bold:false}
execute if score #pat tk matches 5 run data modify storage rlk:mboss sub append value {text:"  ·  연속기 · 블링크",color:"#E8E2D0",bold:false}
execute if score #pat tk matches 6 run data modify storage rlk:mboss sub append value {text:"  ·  연속기 · 블링크 Ⅱ",color:"#E8E2D0",bold:false}
execute if score #pat tk matches 7 run data modify storage rlk:mboss sub append value {text:"  ·  붉은 핵 연속기",color:"#E8E2D0",bold:false}
execute if score #pat tk matches 50 run data modify storage rlk:mboss sub append value {text:"  ·  원소 전환",color:"#E8E2D0",bold:false}
