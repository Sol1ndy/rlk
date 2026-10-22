# The name-line badges (plan 4.11): ◈<leg> ◈<tail> (dim #707070 until absorbed, then the element colour) and
# ◈낙인 while branded. The framework draws "Lv.N 야타용왕" itself.
data modify storage rlk:mboss extra set value []
execute if score #azLeg mb matches 1 if score #azPh mb matches ..1 run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#707070"},{text:"불",color:"#707070"}]}
execute if score #azLeg mb matches 1 if score #azPh mb matches 2.. run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#FF8A3D"},{text:"불",color:"#FF8A3D"}]}
execute if score #azLeg mb matches 2 if score #azPh mb matches ..1 run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#707070"},{text:"물",color:"#707070"}]}
execute if score #azLeg mb matches 2 if score #azPh mb matches 2.. run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#4FB8FF"},{text:"물",color:"#4FB8FF"}]}
execute if score #azTail mb matches 3 unless score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#707070"},{text:"번개",color:"#707070"}]}
execute if score #azTail mb matches 3 if score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#C58BFF"},{text:"번개",color:"#C58BFF"}]}
execute if score #azTail mb matches 4 unless score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#707070"},{text:"얼음",color:"#707070"}]}
execute if score #azTail mb matches 4 if score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#9FE8F5"},{text:"얼음",color:"#9FE8F5"}]}
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=1}] run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#FF8A3D"},{text:"낙인",color:"#FF8A3D"}]}
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=2}] run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#4FB8FF"},{text:"낙인",color:"#4FB8FF"}]}
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=3}] run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#C58BFF"},{text:"낙인",color:"#C58BFF"}]}
execute if entity @a[tag=player,scores={azBrT=1..,azBrE=4}] run data modify storage rlk:mboss extra append value {text:"",extra:[{text:" "},{text:"",font:"rlk:mboss_az",color:"#9FE8F5"},{text:"낙인",color:"#9FE8F5"}]}
