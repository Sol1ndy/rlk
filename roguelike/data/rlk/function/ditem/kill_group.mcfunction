$kill @e[tag=rlk_ditem,scores={dgid=$(dg)}]
$kill @e[tag=rlk_dinfo,scores={dgid=$(dg)}]
$kill @e[tag=rlk_dbtn,scores={dgid=$(dg)}]
$kill @e[tag=rlk_dlbl,scores={dgid=$(dg)}]
$data remove storage rlk:ditems records.k$(dg)
