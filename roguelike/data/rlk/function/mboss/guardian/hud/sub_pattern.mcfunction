function rlk:mboss/guardian/hud/extra
execute if score #gdPick mb matches 1 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"공간 찌르기",color:"#FFD86B"}]
execute if score #gdPick mb matches 2 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"공간 투창",color:"#FFD86B"}]
execute if score #gdPick mb matches 3 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"공간을 집행하는 시련",color:"#FFD86B"}]
execute if score #gdPick mb matches 4 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"어둠 속에서 퍼지는 공간",color:"#FFD86B"}]
execute if score #gdPick mb matches 5 run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"하늘을 심판하는 자",color:"#FFD86B"}]
