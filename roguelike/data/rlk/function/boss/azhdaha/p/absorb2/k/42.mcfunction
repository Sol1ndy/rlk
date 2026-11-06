# absorb2 #azPT 42
function rlk:boss/azhdaha/look/tail
function rlk:boss/azhdaha/arena/look_tail
function rlk:boss/azhdaha/svc/banner_ab2
function rlk:mboss/line/say {t:"모락스! 너 정말 날 파멸시킬 작정이냐!",c:"#F2B53A",gap:2,hold:50,snd:2}
function rlk:boss/azhdaha/svc/phase_3
function rlk:mboss/push/ring {r:80,to:85,kb:4}
execute if score #azTail mb matches 3 run function rlk:boss/azhdaha/fx/snd/absorb_burst/3
execute if score #azTail mb matches 4 run function rlk:boss/azhdaha/fx/snd/absorb_burst/4
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azTail mb matches 3 run function rlk:boss/azhdaha/fx/p/impact/3
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azTail mb matches 4 run function rlk:boss/azhdaha/fx/p/impact/4
function rlk:boss/azhdaha/fx/p/shock_dome {r:80}
execute if score #azTail mb matches 3 run execute at @s rotated as @s rotated ~ 0 positioned ^0 ^3.956 ^-0.258 run function rlk:boss/azhdaha/fx/p/bolt
execute if score #azTail mb matches 3 run function rlk:boss/azhdaha/fx/hud/flash_violet
execute if score #azTail mb matches 4 run function rlk:boss/azhdaha/fx/hud/flash_white
