# macro: e = 각인 id
$data modify storage rlk:eng cur set from storage rlk:engravings registry.$(e)
$execute store result score #n tmp run scoreboard players get $(e) engN
execute store result storage rlk:eng cur.n int 1 run scoreboard players get #n tmp
function rlk:root/card3 with storage rlk:eng cur
