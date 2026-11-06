# 추가 설명(info.extra: 이름 + 설명 줄)을 고유 특성 종이의 설명 아래에 붙인다
execute if data storage rlk:chars pas.passive[0] run data modify storage rlk:chars pas.passive append value {text:"",italic:false}
data modify storage rlk:chars pas.passive append value {text:"",italic:false,bold:true,color:"white"}
data modify storage rlk:chars pas.passive[-1].text set from storage rlk:chars cur.info.extra.name
data modify storage rlk:chars pas.passive[-1].color set from storage rlk:chars cur.info.color
data modify storage rlk:chars pas.passive append from storage rlk:chars cur.info.extra.lore[]
