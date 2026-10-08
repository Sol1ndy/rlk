# 단계마다: 개수를 채웠으면 밝은 설명 줄, 아니면 어두운 설명 줄
execute unless data storage rlk:eng tq[0] run return 0
function rlk:engravings/info_tier with storage rlk:eng tq[0]
function rlk:engravings/info_lines
data remove storage rlk:eng tq[0]
function rlk:engravings/info_tiers
