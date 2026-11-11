# The repel ended (@s = body): cine off. After G1: balance + 3, P2 at once (first decision after
# 20 t; no down window). After G2: the lethal true hit if its kick did not land (it normally kills at
# 129: death_start took over before this).
function rlk:mboss/cine/end
execute if score #ph hr matches 10 run return run function rlk:boss/scarlet/core/kill
function rlk:boss/scarlet/core/bal/repel
function rlk:boss/scarlet/core/p2/from_repel
