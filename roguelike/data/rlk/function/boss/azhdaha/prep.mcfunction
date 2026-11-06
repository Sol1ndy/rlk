# Hook prep (cm.md 5.3; @s = the kind-9 zone marker, at it; once per entrance build): roll the element pair
# (plan 4.1: 0 불/번개 1 물/얼음 2 불/얼음 3 물/번개), write cprep.azhdaha (pair, gate label, title, sub),
# the pair on the zone marker (data.az_pair), the two glyph props on the entrance stele (upper = tail, lower =
# leg), the stele glow chain (every 10 t while the props live).
execute store result score #azPair mb run random value 0..3
execute if score #azPair mb matches 0 run function rlk:boss/azhdaha/prep/pair_0
execute if score #azPair mb matches 1 run function rlk:boss/azhdaha/prep/pair_1
execute if score #azPair mb matches 2 run function rlk:boss/azhdaha/prep/pair_2
execute if score #azPair mb matches 3 run function rlk:boss/azhdaha/prep/pair_3
function rlk:boss/azhdaha/prep/glyphs
schedule function rlk:boss/azhdaha/prep_glow 10t replace
