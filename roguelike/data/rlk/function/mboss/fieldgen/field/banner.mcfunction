# Field opening clock 56: the banner "중력이 감소하고 점프 능력이 향상됩니다" and low gravity (#fgLowG -> #mbLowG every tick).
scoreboard players set #fgLowG mb 1
function rlk:mboss/line/say {t:"중력이 감소하고 점프 능력이 향상됩니다",c:"#D9C8FF",gap:1,hold:50,snd:1}
function rlk:mboss/fieldgen/cfx/banner
