# gid 의 각인마다: (두 번째부터 빈 줄) + "◆ 이름" + 단계 설명 (#n tmp = 묶음의 개수). #gk = 각인 수
execute unless data storage rlk:eng gid[0] run return 0
execute if score #gk eng matches 1.. run data modify storage rlk:eng lore append value {text:"",italic:false}
data modify storage rlk:eng e set from storage rlk:eng gid[0]
function rlk:engravings/info_gitem_one with storage rlk:eng
scoreboard players add #gk eng 1
data remove storage rlk:eng gid[0]
function rlk:engravings/info_gitem_lines
