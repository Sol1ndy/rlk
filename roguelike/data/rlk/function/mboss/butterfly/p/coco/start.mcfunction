# B4 달빛 축복 (clip coco: wrap 5, orbs (19, 46), ball 30-42; orb pj 0.25 b/t, steer 9/t for
# 40 t, burst decal r 2.8 at +40, burst +50; end 98 or earlier once both orbs are gone).
function rlk:mboss/butterfly/rig_stub/face/player
execute unless entity @e[tag=rlk_body,distance=..6.5,limit=1] run function rlk:mboss/butterfly/wx/u/toward {d:0.3}
