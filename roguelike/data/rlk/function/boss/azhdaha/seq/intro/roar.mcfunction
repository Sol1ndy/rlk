# The roar: radial gold leaves, a shock dome, the line, the phase-1 music.
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2 run function rlk:boss/azhdaha/fx/p/gold_leaves
function rlk:boss/azhdaha/fx/p/shock_dome {r:120}
function rlk:boss/azhdaha/fx/snd/intro_roar
function rlk:mboss/line/say {t:"인간 주제에, 선을 넘지 마라!",c:"#F2B53A",gap:2,hold:50,snd:2}
function rlk:boss/azhdaha/svc/music_1
