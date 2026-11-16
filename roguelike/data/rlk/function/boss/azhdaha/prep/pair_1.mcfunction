# Pair 1: legs hydro (물, phase 2), tail cryo (얼음, phase 3).
data modify storage rlk:mboss cprep.azhdaha.pair set value {leg:2,tail:4,i:1}
data modify storage rlk:mboss cprep.azhdaha.gate set value {item:"minecraft:paper",model:"rlk:mboss/az_kit/glyph_cryo",item2:"minecraft:paper",model2:"rlk:mboss/az_kit/glyph_hydro",l1:{text:"야타용왕",color:"#F2B53A",bold:true},l2:[{text:"흡수 원소: ",color:"#C8C0B0",bold:false},{text:"물",color:"#4FB8FF",bold:false},{text:" (다리 · 2페이즈) · ",color:"#C8C0B0",bold:false},{text:"얼음",color:"#9FE8F5",bold:false},{text:" (꼬리 · 3페이즈)",color:"#C8C0B0",bold:false}],l3:{text:"내성: 물리 · 바위 · 물 · 얼음 30% · 그 외 10%",color:"#B0B0B0",bold:false},n:10}
data modify storage rlk:mboss cprep.azhdaha.title set value {text:"야타용왕",color:"#F2B53A",bold:true}
data modify storage rlk:mboss cprep.azhdaha.sub set value {text:"봉인된 바위 용의 왕 · 물 / 얼음",color:"#E8E2D0",bold:false}
data modify entity @s data.az_pair set value {leg:2,tail:4,i:1}
