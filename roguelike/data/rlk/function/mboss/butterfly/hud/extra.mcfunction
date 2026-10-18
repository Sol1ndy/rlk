# Name-line suffix: form, groggy, the 달빛 고치 badge (maroon pill, salmon swirl) or the reward star.
data modify storage rlk:mboss extra set value []
execute if score #bfForm mb matches 1 run data modify storage rlk:mboss extra append value {text:"   인간형",color:"#C8E6A0",bold:false}
execute if score #bfForm mb matches 2 run data modify storage rlk:mboss extra append value {text:"   나비형",color:"#B6E35A",bold:false}
execute if score #bfSt mb matches 3..4 run data modify storage rlk:mboss extra append value {text:"  · 그로기",color:"#9FE8A0",bold:false}
execute if score #bfCoc mb matches 1 run data modify storage rlk:mboss extra append value {text:"  ◖",color:"#8C525C",bold:false}
execute if score #bfCoc mb matches 1 run data modify storage rlk:mboss extra append value {text:"꩜",color:"#E8858A",bold:true}
execute if score #bfCoc mb matches 1 run data modify storage rlk:mboss extra append value {text:"◗",color:"#8C525C",bold:false}
execute if score #bfBuff mb matches 1 run data modify storage rlk:mboss extra append value {text:"  ✦",color:"#F4E28A",bold:true}
