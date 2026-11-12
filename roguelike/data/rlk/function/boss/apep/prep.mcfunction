# Hook prep (cm.md 5.3; @s = the kind-9 zone marker, at it; once per entrance build; cb/pp/apep cleared
# cprep.apep first): the gate texts (ap_contract 0.6.7), the title / sub of the gate press, the two gate crystals
# (theme entrance_layout glyphs; rlk_room props: room/clear removes them) in the kit look fx/prop/gate_crystal
# (AP-FIX RV-06; the model's foot is its origin, so it stands on the floor).
data modify storage rlk:mboss cprep.apep.gate set value {item:"minecraft:pitcher_plant",model:"minecraft:pitcher_plant",item2:"minecraft:emerald",model2:"rlk:mboss/ap_kit/gate_crystal",l1:{text:"아펩의 오아시스 파수꾼",color:"#C9C452",bold:true},l2:{text:"내성: 풀 30% · 그 외 10%",color:"#D0D0D0",bold:false},l3:{text:"챕터 3 보스",color:"#A8A8A8",bold:false},n:11}
data modify storage rlk:mboss cprep.apep.title set value {text:"아펩의 오아시스 파수꾼",color:"#C9C452",bold:true}
data modify storage rlk:mboss cprep.apep.sub set value {text:"종막 오아시스 파수꾼",color:"#E8E2D0",bold:false}
kill @e[type=minecraft:item_display,tag=rlk_mb_ap_gate]
summon minecraft:item_display ~3.5 201 ~12.5 {Tags:["rlk_room","rlk_mb_ap_gate"],Rotation:[0f,0f],billboard:"fixed",brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.2f,1.2f]},item:{id:"minecraft:emerald",count:1}}
summon minecraft:item_display ~-3.5 201 ~12.5 {Tags:["rlk_room","rlk_mb_ap_gate"],Rotation:[0f,0f],billboard:"fixed",brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.2f,1.2f]},item:{id:"minecraft:emerald",count:1}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_gate,distance=..48] run function rlk:boss/apep/fx/prop/gate_crystal
