# 각인 선택지 셋 → rlk:room rootc (각인 id 목록). 가진 각인(개수 1 이상) 중에서 무작위, 셋이 안 되면 나머지는 가지지 않은 각인에서 무작위
# 카드마다 함께 줄 아이템도 이때 정해 rlk:room rooti (rootc 와 같은 순서)에 둔다
scoreboard players operation #rootRolled room = #rootG room
data modify storage rlk:room rootc set value []
data modify storage rlk:room rown set value []
data modify storage rlk:room roth set value []
data modify storage rlk:room wq set from storage rlk:engravings ids
function rlk:root/split_loop
data modify storage rlk:room rq set from storage rlk:room rown
function rlk:root/take_loop
data modify storage rlk:room rq set from storage rlk:room roth
function rlk:root/take_loop
function rlk:root/roll_items
