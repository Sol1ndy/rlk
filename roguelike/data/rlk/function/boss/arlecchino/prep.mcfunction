# Hook prep (@s = the kind-9 entrance zone marker, at it; cb/pp/arlecchino cleared cprep.arlecchino first): the gate
# texts, the title / sub of the gate press, the crimson flames on the gravestone (the theme's GRAVE offset; a
# self-rescheduling chain that stops when the anchor is gone; uninstall clears the schedule).
data modify storage rlk:mboss cprep.arlecchino.gate set value {item:"minecraft:netherite_hoe",model:"rlk:mboss/kn_kit/gate_icon",item2:"minecraft:red_candle",model2:"minecraft:red_candle",l1:{text:"추억: 빛과 그림자의 결별",color:"#D0D0D0",bold:false},l2:{text:"「아를레키노」",color:"#E0303A",bold:true},l3:{text:"영락한 폐허",color:"#A8A8A8",bold:false},n:12}
data modify storage rlk:mboss cprep.arlecchino.title set value {text:"「아를레키노」",color:"#E0303A",bold:true}
data modify storage rlk:mboss cprep.arlecchino.sub set value {text:"우인단 집행관 서열 4위",color:"#E8E2D0",bold:false}
kill @e[type=minecraft:marker,tag=rlk_kn_grave]
summon minecraft:marker ~0 ~4.3 ~-4.5 {Tags:["rlk_room","rlk_kn_grave"]}
schedule function rlk:boss/arlecchino/gate/flames 10t replace
