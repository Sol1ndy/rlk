# A transition step finished: the next one.
execute if score #azTr mb matches 2 run return run function rlk:boss/azhdaha/tr/to_slide
execute if score #azTr mb matches 3 if score #azTrN mb matches 1 run return run function rlk:boss/azhdaha/tr/to_abs1
execute if score #azTr mb matches 3 if score #azTrN mb matches 2 run return run function rlk:boss/azhdaha/tr/to_abs2
execute if score #azTr mb matches 4 if score #azTrN mb matches 1 run return run function rlk:boss/azhdaha/tr/done
execute if score #azTr mb matches 4 if score #azTrN mb matches 2 run return run function rlk:boss/azhdaha/tr/to_b3
function rlk:boss/azhdaha/tr/done
