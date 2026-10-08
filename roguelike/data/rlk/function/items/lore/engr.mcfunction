# 각인 줄: "각인  수호 · 원소" (storage rlk:io src.engravings)
data modify storage rlk:io engx set value []
data modify storage rlk:io engq set from storage rlk:io src.engravings
function rlk:items/lore/engr_loop
data modify storage rlk:io lore append value {text:"",italic:false}
function rlk:items/lore/engr_put with storage rlk:io
