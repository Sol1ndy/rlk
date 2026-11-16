# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# Strike 1 only: the title with the instant-kill warning and the red line (the lose shows 「소생 실패」 alone;
# AP-FIX RV-09).
function rlk:boss/apep/fx/hud/title {g:"fail",t:"「소생 실패」",c:"#C36E5A",s:"다시 한 번 실패하면 쓰러집니다",hold:50}
function rlk:mboss/line/say {t:"다시 한 번 실패하면 쓰러집니다",c:"#C36E5A",gap:2,hold:80,snd:2}
