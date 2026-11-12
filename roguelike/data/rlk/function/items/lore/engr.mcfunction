# 각인 줄: "각인  수호 · 원소" (storage rlk:io src.engravings)
data modify storage rlk:io engx set value []
data modify storage rlk:io engq set from storage rlk:io src.engravings
function rlk:items/lore/engr_loop
# 각인이 없으면 줄을 만들지 않는다(빈 extra 목록은 글자로 만들 수 없음)
execute if data storage rlk:io engx[0] run data modify storage rlk:io lore append value {text:"",italic:false}
execute if data storage rlk:io engx[0] run function rlk:items/lore/engr_put with storage rlk:io
