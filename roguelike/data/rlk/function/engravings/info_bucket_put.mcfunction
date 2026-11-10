# (engravings/info_bucket 에서) rlk:eng e · #n tmp → 묶음 b.n<#c eng> 끝에 {id, n}
data modify storage rlk:eng bt set value {}
data modify storage rlk:eng bt.id set from storage rlk:eng e
execute store result storage rlk:eng bt.n int 1 run scoreboard players get #n tmp
execute if score #c eng matches 1 run data modify storage rlk:eng b.n1 append from storage rlk:eng bt
execute if score #c eng matches 2 run data modify storage rlk:eng b.n2 append from storage rlk:eng bt
execute if score #c eng matches 3 run data modify storage rlk:eng b.n3 append from storage rlk:eng bt
execute if score #c eng matches 4 run data modify storage rlk:eng b.n4 append from storage rlk:eng bt
execute if score #c eng matches 5 run data modify storage rlk:eng b.n5 append from storage rlk:eng bt
execute if score #c eng matches 6 run data modify storage rlk:eng b.n6 append from storage rlk:eng bt
execute if score #c eng matches 7 run data modify storage rlk:eng b.n7 append from storage rlk:eng bt
execute if score #c eng matches 8 run data modify storage rlk:eng b.n8 append from storage rlk:eng bt
execute if score #c eng matches 9 run data modify storage rlk:eng b.n9 append from storage rlk:eng bt
execute if score #c eng matches 10 run data modify storage rlk:eng b.n10 append from storage rlk:eng bt
execute if score #c eng matches 11 run data modify storage rlk:eng b.n11 append from storage rlk:eng bt
execute if score #c eng matches 12 run data modify storage rlk:eng b.n12 append from storage rlk:eng bt
