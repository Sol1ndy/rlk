# Macro {a, d, t}: a marker tagged t (+ rlk_mb_az_xnt) at world yaw a, d blocks from here, on the floor.
$execute rotated $(a) 0 positioned ^ ^ ^$(d) run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xnt","$(t)"]}
