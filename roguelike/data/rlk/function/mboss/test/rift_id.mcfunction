# /function rlk:mboss/test/rift_id {id:"tachy"} (= rlk:boss/test/rift_id): test/rift with a fixed special boss.
# {id:"help"}: the special ids (test/help_rift_id). The work is in rift_id_do (every line here parses with id = help).
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:mboss/test/help_rift_id
$function rlk:mboss/test/rift_id_do {id:"$(id)"}
