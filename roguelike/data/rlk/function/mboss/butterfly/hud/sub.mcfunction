# Third line: what she is doing, then the player's 달빛 고치 / 달빛 축복 받음 state (the kit's hud/put_sub: badge
# glyph + "달빛 고치 — 회복 9/15%" (the cure meter, score components) + the dew icon, or badge + "달빛 축복 받음
# (치명타 +15% · 치명타 피해 +50%)").
execute if score #mbSt mb matches 0 run data modify storage rlk:mboss sub set value []
execute if score #mbSt mb matches 0 run return 0
data modify storage rlk:mboss sub set value [{text:"인간형",color:"#C8E6A0",bold:true}]
execute if score #bfForm mb matches 2 run data modify storage rlk:mboss sub set value [{text:"나비형",color:"#B6E35A",bold:true}]
execute if score #bfForm mb matches 2 if score #bfLook mb matches 1 run data modify storage rlk:mboss sub append value {text:"  화염 날개",color:"#FFB070"}
execute if score #bfForm mb matches 2 if score #bfLook mb matches 7 run data modify storage rlk:mboss sub append value {text:"  달빛 날개",color:"#D9F5A8"}
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 1 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"달빛 발차기",color:"#D9F5A8"}]
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 2 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"달빛 점프",color:"#D9F5A8"}]
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 3 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"달빛 돌진",color:"#D9F5A8"}]
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 4 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"광폭한 진공",color:"#D9F5A8"}]
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 11 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"우아한 날개",color:"#D9F5A8"}]
execute if score #bfSt mb matches 5 if score #bfPick mb matches 11 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"우아한 날개",color:"#D9F5A8"}]
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 12 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"화염 날개의 습격",color:"#FFB070"}]
execute if score #bfSt mb matches 5 if score #bfPick mb matches 12 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"화염 날개의 습격",color:"#FFB070"}]
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 13 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"날개 휩쓸개",color:"#FFB070"}]
execute if score #bfSt mb matches 5 if score #bfPick mb matches 13 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"날개 휩쓸개",color:"#FFB070"}]
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 14 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"달빛 축복",color:"#D9F5A8"}]
execute if score #bfSt mb matches 5 if score #bfPick mb matches 14 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"달빛 축복",color:"#D9F5A8"}]
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 15 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"달빛 해제",color:"#D9F5A8"}]
execute if score #bfSt mb matches 5 if score #bfPick mb matches 15 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"달빛 해제",color:"#D9F5A8"}]
execute if score #bfSt mb matches 1..2 if score #bfPick mb matches 20 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"변신",color:"#E8858A"}]
execute if score #bfSt mb matches 3 run data modify storage rlk:mboss sub set value [{text:"그로기",color:"#9FE8A0",bold:true}]
execute if score #bfSt mb matches 4 run data modify storage rlk:mboss sub set value [{text:"그로기  ",color:"#9FE8A0",bold:true},{text:"다시 일어선다",color:"#C8E8C8"}]
function rlk:mboss/butterfly/fx/hud/put_sub
