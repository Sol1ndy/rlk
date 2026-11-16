# Test 24: the break now (as a counter inside a window: cancel, true damage, stun).
execute if score #mbSt mb matches 0 run function rlk:boss/arlecchino/core/intro/done
execute if score #pat kn matches 51.. run return 0
function rlk:boss/arlecchino/core/break
