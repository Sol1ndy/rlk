# The props of the current look (#cpLook: 0 plain, 1 lit).
execute if score #cpLook mb matches 0 run return run function rlk:mboss/cproto/props/plain
execute if score #cpLook mb matches 1 run return run function rlk:mboss/cproto/props/lit
function rlk:mboss/cproto/props/plain
