data modify storage rlk:mboss hzs set from storage rlk:mboss hzp
data modify storage rlk:mboss hzs.col set from storage rlk:mboss hzc[10]
data modify storage rlk:mboss hzs.sc set value "1.3"
function rlk:mboss/hz/d/full_safe2 with storage rlk:mboss hzs
