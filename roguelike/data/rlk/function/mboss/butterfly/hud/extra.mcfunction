# Name-line suffix: form, groggy, then the kit's badges (hud/put_extra: the 달빛 고치 glyph, maroon disc with a
# salmon swirl, and / or the 달빛 축복 받음 glyph; flags set by fx/hud/coc_on|off, buff_on|off).
data modify storage rlk:mboss extra set value []
execute if score #bfForm mb matches 1 run data modify storage rlk:mboss extra append value {text:"   인간형",color:"#C8E6A0",bold:false}
execute if score #bfForm mb matches 2 run data modify storage rlk:mboss extra append value {text:"   나비형",color:"#B6E35A",bold:false}
execute if score #bfSt mb matches 3..4 run data modify storage rlk:mboss extra append value {text:"  · 그로기",color:"#9FE8A0",bold:false}
function rlk:mboss/butterfly/fx/hud/put_extra
