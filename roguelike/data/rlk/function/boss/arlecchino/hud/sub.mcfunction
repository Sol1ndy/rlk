# The boss-bar third line (@s any; on every state change): the phase sub (우인단 집행관 서열 4위 / 페르엘) or the
# running pattern name, then the badge ◆선혈의 충격 while armed (names / the badge only; PLAN §4.6).
data modify storage rlk:mboss sub set value [{text:"우인단 집행관 서열 4위",color:"#E8E2D0",bold:false}]
execute if score #ph kn matches 5.. run data modify storage rlk:mboss sub set value [{text:"페르엘",color:"#E8E2D0",bold:false}]
execute if score #pat kn matches 1 run data modify storage rlk:mboss sub set value [{text:"사형장으로의 초대",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 2 run data modify storage rlk:mboss sub set value [{text:"사형장으로의 초대",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 3 run data modify storage rlk:mboss sub set value [{text:"붉은 달의 낫",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 4 run data modify storage rlk:mboss sub set value [{text:"붉은 달의 낫",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 5 run data modify storage rlk:mboss sub set value [{text:"불꽃 도약",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 6 run data modify storage rlk:mboss sub set value [{text:"불꽃 도약",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 7 run data modify storage rlk:mboss sub set value [{text:"블러드 돌진",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 8 run data modify storage rlk:mboss sub set value [{text:"블러드 돌진",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 9 run data modify storage rlk:mboss sub set value [{text:"와리가리 베기",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 10 run data modify storage rlk:mboss sub set value [{text:"붉은 피의 연회",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 11 run data modify storage rlk:mboss sub set value [{text:"죽음의 칼날",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 12 run data modify storage rlk:mboss sub set value [{text:"연옥 그림자 분신",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 13 run data modify storage rlk:mboss sub set value [{text:"사형장으로의 초대",color:"#E8E2D0",bold:true}]
execute if score #pat kn matches 20 run data modify storage rlk:mboss sub set value [{text:"재가 된 만상",color:"#E8E2D0",bold:true}]
execute if score #shock kn matches 1 run data modify storage rlk:mboss sub append value {text:"  ◆선혈의 충격",color:"#FF3A4A",bold:true}
