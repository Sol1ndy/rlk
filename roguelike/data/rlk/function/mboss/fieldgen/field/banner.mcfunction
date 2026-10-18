# Field opening clock 56: low gravity (#fgLowG -> #mbLowG every tick), the kit's banner "중력이 감소하고 점프 능력이 향상됩니다"
# (actionbar 80 t, the big icon, its sound; the start gametime #fgBanG lets a break / cut drop it early), the
# low-gravity icon on the name line, the typed caption. Once per field (fix round FG-S2): #fgBanF = the field
# number #fgFN whose banner played, so a reload or a test request inside the field does not play it again.
execute if score #fgBanF mb = #fgFN mb run return 0
scoreboard players operation #fgBanF mb = #fgFN mb
scoreboard players set #fgLowG mb 1
function rlk:mboss/fieldgen/fx/hud/banner_field
execute store result score #fgBanG mb run time query gametime
function rlk:mboss/fieldgen/fx/hud/lowg_on
function rlk:mboss/line/say {t:"중력이 감소하고 점프 능력이 향상됩니다",c:"#D9C8FF",gap:1,hold:50,snd:1}
function rlk:mboss/fieldgen/seq_f/banner
