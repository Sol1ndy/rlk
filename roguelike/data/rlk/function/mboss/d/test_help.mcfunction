# GENERATED dispatcher: rlk:<fn root>/test/help of the running boss (#mbId mb = registry n; from test/help_pattern).
execute if score #mbId mb matches 1 run return run function rlk:mboss/guardian/test/help
execute if score #mbId mb matches 2 run return run function rlk:mboss/butterfly/test/help
execute if score #mbId mb matches 3 run return run function rlk:mboss/fieldgen/test/help
execute if score #mbId mb matches 99 run return run function rlk:mboss/proto/test/help
execute if score #mbId mb matches 98 run return run function rlk:mboss/cproto/test/help
execute if score #mbId mb matches 10 run return run function rlk:boss/azhdaha/test/help
execute if score #mbId mb matches 11 run return run function rlk:boss/apep/test/help
execute if score #mbId mb matches 97 run return run function rlk:mboss/spproto/test/help
tellraw @s ["",{text:" 이 보스의 패턴 번호 목록이 없습니다.",color:"gray"}]
