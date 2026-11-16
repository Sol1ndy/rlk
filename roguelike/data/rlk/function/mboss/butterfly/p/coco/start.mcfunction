# B4 달빛 축복 (clip coco: wrap 3, orbs (14, 34), ball 22-30; orb pj 0.25 b/t, steer 9/t for
# 40 t, burst hazard r 2.8 at +40 (quiet), burst +50; end 86 or earlier once both orbs are gone).
function rlk:mboss/butterfly/rig/face/player
execute unless entity @e[tag=rlk_body,distance=..6.5,limit=1] run function rlk:mboss/butterfly/wx/u/toward {d:0.3}
