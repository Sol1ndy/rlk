$data modify entity @e[tag=rlk_pk_tip2,limit=1] text set value {text:"",extra:$(tip)}
# 가운데 맞춤: 줄 수의 절반만큼 아래로
execute store result entity @e[tag=rlk_pk_tip2,limit=1] transformation.translation[1] float -0.029 run data get storage rlk:lvpick tip
