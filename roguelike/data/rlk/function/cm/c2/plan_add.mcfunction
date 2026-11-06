$data modify storage rlk:c2 plan append value {id:"$(id)",n:0}
execute store result storage rlk:c2 plan[-1].n int 1 run scoreboard players get #c2n tmp
