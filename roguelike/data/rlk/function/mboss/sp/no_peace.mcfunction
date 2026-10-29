# The rift was entered on peaceful (@s = its anchor): no fight. Returns 0.
tellraw @a[tag=player] [{text:"[특수 보스] ",color:"#E0703A",bold:true},{text:"난이도가 '평화로움'이면 특수 보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 들어가세요.",color:"gray",bold:false}]
return 0
