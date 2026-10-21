# /reload inside absorb 1: it finishes at once (plan 4.3): the looks, phase 2, targetable again.
execute if score #azPT mb matches ..93 run function rlk:mboss/azhdaha/svc/phase_2
# (FIX STATE-6) the leg special that opens phase 2 (plan 5 T2) was not cast yet, or its cast part is cut by
# the core reload (orbs not out yet): the first phase-2 decision runs it (service 30 with its own roar)
execute if score #azPT mb matches ..93 unless score #azBgL mb matches 31 run function rlk:mboss/azhdaha/p/absorb1/requeue
execute if score #azPT mb matches 94.. if score #azCast mb matches 31..32 unless score #azBgL mb matches 31 run function rlk:mboss/azhdaha/p/absorb1/requeue
function rlk:mboss/azhdaha/look/legs
function rlk:mboss/azhdaha/arena/look_leg
function rlk:mboss/azhdaha/svc/cine_off
function rlk:mboss/azhdaha/rig/glow/gold_off
function rlk:mboss/azhdaha/px/normal
function rlk:mboss/azhdaha/svc/banner_brand
function rlk:mboss/azhdaha/p/end
