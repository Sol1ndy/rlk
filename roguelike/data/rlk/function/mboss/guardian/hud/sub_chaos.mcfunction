function rlk:mboss/guardian/hud/extra
data modify storage rlk:mboss sub set value [{text:"혼돈  ",color:"#E03A3A",bold:true},{text:"원소별 ",color:"#E8B8B8"}]
execute if score #gdSa1 mb matches 0 run data modify storage rlk:mboss sub append value {text:"◇ ",color:"#8A8A8A"}
execute if score #gdSa1 mb matches 1 if score #gdSk1 mb matches 1 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#FF8A4C"}
execute if score #gdSa1 mb matches 1 if score #gdSk1 mb matches 2 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#5CC8FF"}
execute if score #gdSa1 mb matches 1 if score #gdSk1 mb matches 3 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#D282FA"}
execute if score #gdSa1 mb matches 1 if score #gdSk1 mb matches 4 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#A2FEFD"}
execute if score #gdSa1 mb matches 1 if score #gdSk1 mb matches 5 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#FCE582"}
execute if score #gdSa1 mb matches 1 if score #gdSk1 mb matches 6 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#A6CEFD"}
execute if score #gdSa2 mb matches 0 run data modify storage rlk:mboss sub append value {text:"◇ ",color:"#8A8A8A"}
execute if score #gdSa2 mb matches 1 if score #gdSk2 mb matches 1 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#FF8A4C"}
execute if score #gdSa2 mb matches 1 if score #gdSk2 mb matches 2 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#5CC8FF"}
execute if score #gdSa2 mb matches 1 if score #gdSk2 mb matches 3 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#D282FA"}
execute if score #gdSa2 mb matches 1 if score #gdSk2 mb matches 4 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#A2FEFD"}
execute if score #gdSa2 mb matches 1 if score #gdSk2 mb matches 5 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#FCE582"}
execute if score #gdSa2 mb matches 1 if score #gdSk2 mb matches 6 run data modify storage rlk:mboss sub append value {text:"✦ ",color:"#A6CEFD"}
data modify storage rlk:mboss sub append value {text:"  남은 시간 ",color:"#E8B8B8",extra:[{score:{name:"#gdTimS",objective:"mb"},color:"#FFFFFF"},{text:"초"}]}
# hint while an active (recorded) star stands: it resists its own element
scoreboard players set #gdHint mb 0
execute if score #gdSa1 mb matches 1 if score #gdSk1 mb matches 1..4 run scoreboard players set #gdHint mb 1
execute if score #gdSa2 mb matches 1 if score #gdSk2 mb matches 1..4 run scoreboard players set #gdHint mb 1
execute if score #gdHint mb matches 1 run data modify storage rlk:mboss sub append value {text:"   기록 원소 별: 같은 원소 40% 내성",color:"#B0A890"}
