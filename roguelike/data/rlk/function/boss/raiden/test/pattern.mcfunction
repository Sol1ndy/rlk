# /function rlk:boss/raiden/test/pattern {id:N} -> test/pattern_do. {id:"help"}: test/help_pattern.
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:boss/raiden/test/help_pattern
$function rlk:boss/raiden/test/pattern_do {id:$(id)}
