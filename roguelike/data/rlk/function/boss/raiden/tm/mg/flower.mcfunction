# @s = the boss: the 추모의 꽃다발 at the centre (hit target: 1 electro / 4 other hits, its gauge above it) and the prompt.
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/object/create {kind:3,model:"remembrance_flower",hp:4,id:1,y:0.05}
kill @e[tag=rlk_rd_orb_body]
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/rig/prop/flower
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm_flower
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/snd/mangeop_flower
function rlk:boss/raiden/judgment_hint
