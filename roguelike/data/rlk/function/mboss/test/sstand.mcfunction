# @s = the test rift's anchor, at it, rotated toward the room centre: the player (and the fall marker) 3.5 b in front of it
# when that spot has free feet and head over a floor, else 2 b (inside the anchor's checked footprint), facing the rift.
execute positioned ^ ^ ^3.5 if block ~ ~ ~ #rlk:dash_pass if block ~ ~1 ~ #rlk:dash_pass unless block ~ ~-1 ~ #rlk:dash_pass run return run function rlk:mboss/test/sstand_at
execute positioned ^ ^ ^2 run function rlk:mboss/test/sstand_at
