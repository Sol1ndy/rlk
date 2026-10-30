# {title,sub,color}: the fight's title (boss bar name line) and sub (gate subtitle); the bars pick it up next tick.
$data modify storage rlk:mboss cur.title set value {text:"$(title)",color:"$(color)",bold:true}
$data modify storage rlk:mboss cur.sub set value "$(sub)"
