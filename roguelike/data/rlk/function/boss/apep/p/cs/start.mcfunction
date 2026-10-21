# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# The CS (plan 7.7, 192 t): the progress is full: every organism wilts (the green pulse ring; no progress), walls and
# libraries cleared, cine; the success line; the Heart blazes (0-24, gold dripping), then lifts out of the cradle (heart_lift);
# t24 the white-out (28 t held): the lush arena, the body unparked (hidden), the phase-3 pool, the p3 look
# UPRIGHT, the push ring; t30 the cradle gone; t32 the rig revival (hidden to t92); t64 the 「불씨」 ember;
# t76 the egg turns green in the wrapping hand; t80 the green flash + the 25 % heal; t92 the Warden bursts out
# (the orb fades into it); t132 the phase-3 title + music 3; t150 cine off; t192 phase 3.
function rlk:boss/apep/svc/phase_cs
scoreboard players set #apStage mb 0
function rlk:boss/apep/org/burst_all
function rlk:boss/apep/org/clear
function rlk:boss/apep/wall/clear
function rlk:boss/apep/svc/lib_clear
function rlk:boss/apep/svc/cine_on
function rlk:mboss/line/say {t:"오아시스의 심장이 소생했습니다",c:"#EDCF63",gap:2,hold:60,snd:2}
function rlk:boss/apep/fx/hud/title {g:"success",t:"오아시스의 심장이 소생했습니다",c:"#EDCF63",s:"",hold:14}
execute positioned 440 201 8 run function rlk:boss/apep/fx/p/wilt_ring
execute positioned 440 201 8 run function rlk:boss/apep/fx/snd/cs_complete
function rlk:boss/apep/om/heart/play/heart_blaze
scoreboard players set #apPLen mb 192
