# Name-line suffix: 순항 (gold) in cruise, 역장 (violet) during the warp and the pack-up; the kit's flags
# (put_extra) supply the rest: " · 역장" + the badge while the meter is open, the low-gravity icon, " · 그로기"
# (the break, groggy and recovery).
data modify storage rlk:mboss extra set value []
execute if score #fgField mb matches 0 run data modify storage rlk:mboss extra append value {text:"   순항",color:"#E8C46A",bold:false}
execute if score #fgField mb matches 1.. unless score #fgOpen mb matches 1 run data modify storage rlk:mboss extra append value {text:"   역장",color:"#9C86E8",bold:false}
function rlk:mboss/fieldgen/fx/hud/put_extra
