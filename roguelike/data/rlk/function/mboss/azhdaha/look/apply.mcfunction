# The looks of #azPh (reload, tests): phase >= 2 legs, phase 3 the tail too.
function rlk:mboss/azhdaha/look/geo
execute if score #azPh mb matches 2..3 run function rlk:mboss/azhdaha/look/legs
execute if score #azPh mb matches 3 run function rlk:mboss/azhdaha/look/tail
