$data modify entity @e[tag=rlk_pk_tip,limit=1] text set value {text:"",extra:$(tip)}
# 길이(요소 수 ≈ 줄 수 × 2)에 따라: ..60 = 글자 0.42 · 줄 폭 230 / 61..80 = 글자 0.42 · 줄 폭 300 / 81.. = 글자 0.36 · 줄 폭 300 (화면 안에 들어오게)
execute store result score #tn tmp run data get storage rlk:lvpick tip
execute if score #tn tmp matches ..60 run data merge entity @e[tag=rlk_pk_tip,limit=1] {line_width:230,transformation:{scale:[0.42f,0.42f,0.42f]}}
execute if score #tn tmp matches 61..80 run data merge entity @e[tag=rlk_pk_tip,limit=1] {line_width:300,transformation:{scale:[0.42f,0.42f,0.42f]}}
execute if score #tn tmp matches 81.. run data merge entity @e[tag=rlk_pk_tip,limit=1] {line_width:300,transformation:{scale:[0.36f,0.36f,0.36f]}}
# 가운데 맞춤: 줄 수의 절반만큼 아래로
execute if score #tn tmp matches ..80 store result entity @e[tag=rlk_pk_tip,limit=1] transformation.translation[1] float -0.029 run data get storage rlk:lvpick tip
execute if score #tn tmp matches 81.. store result entity @e[tag=rlk_pk_tip,limit=1] transformation.translation[1] float -0.0249 run data get storage rlk:lvpick tip
