# @s = enemy whose gauge just hit 0: groggy now, or (a boss in a state its module protects) as soon as it allows
execute if score @s balC matches 3 unless function rlk:bal/boss/ok run return run function rlk:bal/boss/pend_on
function rlk:bal/grog/start
