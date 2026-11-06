$data modify storage rlk:c3 plan append value {id:"$(id)",n:0}
execute store result storage rlk:c3 plan[-1].n int 1 run scoreboard players get #c3n tmp
