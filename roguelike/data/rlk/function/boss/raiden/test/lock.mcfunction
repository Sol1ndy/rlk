# /function rlk:boss/raiden/test/lock {id:N} -> test/lock_do. {id:"help"}: test/help_lock.
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:boss/raiden/test/help_lock
$function rlk:boss/raiden/test/lock_do {id:$(id)}
