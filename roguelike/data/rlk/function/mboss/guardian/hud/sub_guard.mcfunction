function rlk:mboss/guardian/hud/extra
data modify storage rlk:mboss sub set value [{text:"파수 모드 ",color:"#FCE484",bold:true}]
execute if score #gdGN mb matches 1 run data modify storage rlk:mboss sub append value {text:"I   ",color:"#FCE484",bold:true}
execute if score #gdGN mb matches 2 run data modify storage rlk:mboss sub append value {text:"II   ",color:"#FCE484",bold:true}
execute if score #gdGP mb matches 3.. run data modify storage rlk:mboss sub append value {text:"휘두르기!",color:"#FFB070",bold:true}
execute if score #gdGP mb matches 3.. run return 0
data modify storage rlk:mboss sub append value {text:"원소 기록  ",color:"#B0A890"}
data modify storage rlk:mboss sub append value {text:"불 ",color:"#FF8A4C",extra:[{score:{name:"#gdN1",objective:"mb"}},{text:"/"},{score:{name:"#gdQ1",objective:"mb"}},{text:"   "}]}
data modify storage rlk:mboss sub append value {text:"물 ",color:"#5CC8FF",extra:[{score:{name:"#gdN2",objective:"mb"}},{text:"/"},{score:{name:"#gdQ2",objective:"mb"}},{text:"   "}]}
data modify storage rlk:mboss sub append value {text:"번개 ",color:"#E484FC",extra:[{score:{name:"#gdN3",objective:"mb"}},{text:"/"},{score:{name:"#gdQ3",objective:"mb"}},{text:"   "}]}
data modify storage rlk:mboss sub append value {text:"얼음 ",color:"#A2FEFD",extra:[{score:{name:"#gdN4",objective:"mb"}},{text:"/"},{score:{name:"#gdQ4",objective:"mb"}},{text:"   "}]}
