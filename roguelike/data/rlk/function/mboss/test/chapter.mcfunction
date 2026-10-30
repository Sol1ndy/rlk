# /function rlk:mboss/test/chapter {id:"cproto"}: test/chapter_ch in the boss's first chapter (none: chapter 1).
# {id:"help"}: the chapter-boss ids (test/help_chapter).
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:mboss/test/help_chapter
$data modify storage rlk:mboss tch set value "$(id)"
execute if data storage rlk:mboss {tch:"cproto"} run return run function rlk:mboss/test/chapter_ch {id:"cproto",ch:1}
execute if data storage rlk:mboss {tch:"azhdaha"} run return run function rlk:mboss/test/chapter_ch {id:"azhdaha",ch:1}
execute if data storage rlk:mboss {tch:"apep"} run return run function rlk:mboss/test/chapter_ch {id:"apep",ch:3}
$function rlk:mboss/test/chapter_ch {id:"$(id)",ch:1}
