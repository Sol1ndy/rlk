# /function rlk:mboss/test/chapter {id:"cproto"}: test/chapter_ch in the boss's first chapter (none: chapter 1).
$data modify storage rlk:mboss tch set value "$(id)"
$function rlk:mboss/test/chapter_ch {id:"$(id)",ch:1}
