# /function rlk:mboss/test/special {id:"tachy"} (= rlk:boss/test/special): test/special_ch in chapter 1.
# {id:"help"}: the special ids (test/help_special).
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:mboss/test/help_special
$function rlk:mboss/test/special_ch {id:"$(id)",ch:1}
