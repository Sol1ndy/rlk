# @s = the kind-9 zone marker of a chapter entrance, at it (from F:room/cboss/<id>/build at zone build): the arena prep
# and the module's prep of the boss named by the zone's data.boss_id (literal lines per boss).
execute if data entity @s data{boss_id:"cproto"} run return run function rlk:mboss/cb/pp/cproto
execute if data entity @s data{boss_id:"azhdaha"} run return run function rlk:mboss/cb/pp/azhdaha
execute if data entity @s data{boss_id:"apep"} run return run function rlk:mboss/cb/pp/apep
