$data modify entity @e[tag=rlk_pk_er,scores={pkIdx=$(row)},limit=1] text set value {text:"",extra:[{text:"$(name)  ",color:"$(color)"},{text:"$(c)",color:"$(nc)",bold:true}]}
