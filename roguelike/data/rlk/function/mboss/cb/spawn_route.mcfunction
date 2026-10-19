# From room/boss_spawn (@s = a kind-9 zone marker with data.cboss, at it): the chapter boss named by data.boss_id.
# No fall-through to Raiden: an unknown boss_id cancels the fight (the gate returns).
execute if data entity @s data{boss_id:"azhdaha"} run return run function rlk:mboss/cb/start {id:"azhdaha"}
function rlk:mboss/start_cancel
