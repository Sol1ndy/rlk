# sorted(많은 순) → groups: 개수가 바뀔 때마다 새 묶음
execute unless data storage rlk:eng sq[0] run return 0
execute store result score #n eng run data get storage rlk:eng sq[0].n
execute unless score #n eng = #gn eng run data modify storage rlk:eng groups append value {ids:[]}
execute unless score #n eng = #gn eng run data modify storage rlk:eng groups[-1].n set from storage rlk:eng sq[0].n
scoreboard players operation #gn eng = #n eng
data modify storage rlk:eng groups[-1].ids append from storage rlk:eng sq[0].id
data remove storage rlk:eng sq[0]
function rlk:engravings/info_group_loop
