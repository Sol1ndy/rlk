# Name-line suffix (D21): the two record slots of this cycle (◇ empty, ◆ element colour) + the state.
data modify storage rlk:mboss extra set value [{text:"   기록 ",color:"#B0A890",bold:false}]
execute if score #gdSlotA mb matches 0 run data modify storage rlk:mboss extra append value {text:"◇",color:"#8A8A8A"}
execute if score #gdSlotA mb matches 1 run data modify storage rlk:mboss extra append value {text:"◆",color:"#FF8A4C"}
execute if score #gdSlotA mb matches 2 run data modify storage rlk:mboss extra append value {text:"◆",color:"#5CC8FF"}
execute if score #gdSlotA mb matches 3 run data modify storage rlk:mboss extra append value {text:"◆",color:"#E484FC"}
execute if score #gdSlotA mb matches 4 run data modify storage rlk:mboss extra append value {text:"◆",color:"#A2FEFD"}
execute if score #gdSlotB mb matches 0 run data modify storage rlk:mboss extra append value {text:"◇",color:"#8A8A8A"}
execute if score #gdSlotB mb matches 1 run data modify storage rlk:mboss extra append value {text:"◆",color:"#FF8A4C"}
execute if score #gdSlotB mb matches 2 run data modify storage rlk:mboss extra append value {text:"◆",color:"#5CC8FF"}
execute if score #gdSlotB mb matches 3 run data modify storage rlk:mboss extra append value {text:"◆",color:"#E484FC"}
execute if score #gdSlotB mb matches 4 run data modify storage rlk:mboss extra append value {text:"◆",color:"#A2FEFD"}
execute if score #gdSt mb matches 3 run data modify storage rlk:mboss extra append value {text:"  · 파수 모드",color:"#FCE484",bold:false}
execute if score #gdSt mb matches 4 run data modify storage rlk:mboss extra append value {text:"  · 혼돈",color:"#E03A3A",bold:false}
execute if score #gdSt mb matches 5 run data modify storage rlk:mboss extra append value {text:"  · 그로기",color:"#9FE8A0",bold:false}
