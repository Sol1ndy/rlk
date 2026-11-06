# @s = the rift's zone marker, after start_go's ret_save: the return point becomes the rift spot (its anchor), 2 b toward the
# room centre when that spot has free feet and head over a floor, else 1.2 b (inside the anchor's checked 3 x 3 footprint;
# the walk-in needs 1 b, so the returning player never stands in the rift), facing the room centre (the anchor's yaw).
scoreboard players operation #spZ mb = @s zid
tag @e[tag=rlk_sp_rr] remove rlk_sp_rr
execute as @e[type=minecraft:marker,tag=rlk_rift] if score @s zid = #spZ mb run tag @s add rlk_sp_rr
execute as @e[type=minecraft:marker,tag=rlk_sp_rr,limit=1] at @s rotated as @s rotated ~ 0 run function rlk:mboss/sp/ret_at
tag @e[tag=rlk_sp_rr] remove rlk_sp_rr
