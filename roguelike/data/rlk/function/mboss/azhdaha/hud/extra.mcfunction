# The name-line badges (plan 4.11): ◈<leg> ◈<tail> (dim #707070 until absorbed, then the element colour) and
# ◈낙인 while branded. The framework draws "Lv.N 야타용왕" itself.
data modify storage rlk:mboss extra set value []
execute if score #azLeg mb matches 1 if score #azPh mb matches ..1 run data modify storage rlk:mboss extra append value {text:"  ◈불",color:"#707070",bold:false}
execute if score #azLeg mb matches 1 if score #azPh mb matches 2.. run data modify storage rlk:mboss extra append value {text:"  ◈불",color:"#FF8A3D",bold:false}
execute if score #azLeg mb matches 2 if score #azPh mb matches ..1 run data modify storage rlk:mboss extra append value {text:"  ◈물",color:"#707070",bold:false}
execute if score #azLeg mb matches 2 if score #azPh mb matches 2.. run data modify storage rlk:mboss extra append value {text:"  ◈물",color:"#4FB8FF",bold:false}
execute if score #azTail mb matches 3 unless score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {text:"  ◈번개",color:"#707070",bold:false}
execute if score #azTail mb matches 3 if score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {text:"  ◈번개",color:"#C58BFF",bold:false}
execute if score #azTail mb matches 4 unless score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {text:"  ◈얼음",color:"#707070",bold:false}
execute if score #azTail mb matches 4 if score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {text:"  ◈얼음",color:"#9FE8F5",bold:false}
execute if entity @a[tag=player,scores={azBrT=1..}] run data modify storage rlk:mboss extra append value {text:"  ◈낙인",color:"#FF6A4A",bold:false}
