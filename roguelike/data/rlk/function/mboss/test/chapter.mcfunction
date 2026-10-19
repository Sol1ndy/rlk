# /function rlk:mboss/test/chapter {id:"cproto"}: test/chapter_ch in the boss's first chapter (none: chapter 1).
$data modify storage rlk:mboss tch set value "$(id)"
execute if data storage rlk:mboss {tch:"cproto"} run return run function rlk:mboss/test/chapter_ch {id:"cproto",ch:1}
execute if data storage rlk:mboss {tch:"azhdaha"} run return run function rlk:mboss/test/chapter_ch {id:"azhdaha",ch:1}
$function rlk:mboss/test/chapter_ch {id:"$(id)",ch:1}
