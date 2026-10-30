# /function rlk:mboss/test/lock {id:N} -> test/lock_do. {id:"help"}: test/help_pattern. The score line lives in lock_do:
# a macro function is instantiated whole, so this one must still parse with id = help.
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:mboss/test/help_pattern
$function rlk:mboss/test/lock_do {id:$(id)}
