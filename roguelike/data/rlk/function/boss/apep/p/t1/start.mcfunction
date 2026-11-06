# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# T1 (plan 7.5, 136 t): sink_revive where it stands (the core plays it at 0; its px sets hide the body); t6
# the libraries cleared; t20 / t30 root chunks; t45 parked, the cradle rises (the gold swirl); t50 the egg lowered;
# t100 the drop (land t106: the beam, the Heart title, progress 2700, music 2, the ley lines); t108 the goal line,
# cine off; t116 wave 1's spawn markers; t136 phase 2.
function rlk:mboss/line/say {t:"종막 오아시스 파수꾼이 땅속으로 숨어듭니다…",c:"#E8E2D0",gap:2,hold:60,snd:2}
function rlk:boss/apep/svc/cine_on
scoreboard players set #apPLen mb 136
execute unless entity 524c4b4d-4150-4800-8000-000000000000 run function rlk:boss/apep/heart/p1_respawn
