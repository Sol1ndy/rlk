# absorb2 #azPT 42
function rlk:mboss/azhdaha/look/tail
function rlk:mboss/azhdaha/arena/look_tail
function rlk:mboss/azhdaha/svc/banner_ab2
function rlk:mboss/line/say {t:"모락스! 너 정말 날 파멸시킬 작정이냐!",c:"#F2B53A",gap:2,hold:50,snd:2}
function rlk:mboss/azhdaha/svc/phase_3
function rlk:mboss/push/ring {r:80,to:85,kb:4}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azTail mb matches 3 run function rlk:mboss/azhdaha/fx/p/shard_rain/3 {r:200,t:48}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run execute if score #azTail mb matches 4 run function rlk:mboss/azhdaha/fx/p/shard_rain/4 {r:200,t:48}
execute if score #azTail mb matches 3 run function rlk:mboss/azhdaha/fx/snd/absorb_burst/3
execute if score #azTail mb matches 4 run function rlk:mboss/azhdaha/fx/snd/absorb_burst/4
execute if score #azTail mb matches 3 run function rlk:mboss/azhdaha/fx/p/recolour/3 {r:280,t:20}
execute if score #azTail mb matches 4 run function rlk:mboss/azhdaha/fx/p/recolour/4 {r:280,t:20}
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azTail mb matches 3 run function rlk:mboss/azhdaha/fx/p/impact/3
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azTail mb matches 4 run function rlk:mboss/azhdaha/fx/p/impact/4
function rlk:mboss/azhdaha/fx/p/shock_dome {r:80}
execute if score #azTail mb matches 3 run execute at @s rotated as @s rotated ~ 0 positioned ^0 ^3.956 ^-0.258 run function rlk:mboss/azhdaha/fx/p/bolt
execute if score #azTail mb matches 3 run function rlk:mboss/azhdaha/fx/hud/flash_violet
execute if score #azTail mb matches 4 run function rlk:mboss/azhdaha/fx/hud/flash_white
execute if score #azTail mb matches 4 run function rlk:mboss/azhdaha/fx/p/frost_burst {r:60}
