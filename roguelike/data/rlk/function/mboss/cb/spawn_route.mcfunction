# From room/boss_spawn (@s = a kind-9 zone marker with data.cboss, at it): the chapter boss named by data.boss_id.
# No fall-through to Raiden: an unknown boss_id cancels the fight (the gate returns).
function rlk:mboss/start_cancel
