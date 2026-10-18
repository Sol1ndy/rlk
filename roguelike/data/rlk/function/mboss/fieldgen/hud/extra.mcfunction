# Name-line suffix: 순항 (gold) / 역장 (violet), · 그로기 during the break, groggy and recovery.
data modify storage rlk:mboss extra set value []
execute if score #fgField mb matches 0 run data modify storage rlk:mboss extra append value {text:"   순항",color:"#E8C46A",bold:false}
execute if score #fgField mb matches 1.. run data modify storage rlk:mboss extra append value {text:"   역장",color:"#9C86E8",bold:false}
execute if score #fgSt mb matches 3..6 run data modify storage rlk:mboss extra append value {text:"  · 그로기",color:"#9FE8A0",bold:false}
