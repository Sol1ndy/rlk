# @s = a camera entity of a dynamic stage after mboss/cam/fix (4 b before its viewpoint along its view): pulled into
# the walk disc as the viewpoint was, and not left lower than 0.3 b over the floor (a lens that looks down at
# something near it: the client looks along the 4-block line from the viewpoint to the entity; in the ground the game
# would cut that line short). The rotation stays: the viewpoint moves by as much as the entity.
function rlk:mboss/ar/clampw
execute store result score #sq_cy hr run data get entity @s Pos[1] 100
execute if score #sq_cy hr matches ..20129 at @s run tp @s ~ 201.3 ~
