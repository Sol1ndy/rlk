# 체험 방 이름표
execute store result storage rlk:lobby lv int 1 run scoreboard players get @a[tag=player,limit=1] level
function rlk:lobby/try/lbl_lv with storage rlk:lobby
execute if score #lobInf lob matches 1 run data modify entity @e[tag=rlk_lk32,limit=1] text set value {"text": "켜짐", "color": "#D0D0D0"}
execute unless score #lobInf lob matches 1 run data modify entity @e[tag=rlk_lk32,limit=1] text set value {"text": "꺼짐", "color": "#D0D0D0"}
execute unless score #lobAura lob matches 1.. run data modify entity @e[tag=rlk_lk33,limit=1] text set value {"text": "없음", "color": "#D0D0D0"}
execute if score #lobAura lob matches 1 run data modify entity @e[tag=rlk_lk33,limit=1] text set value [{"text": "불", "color": "#FF6A3D"}, {"text": " (2초마다)", "color": "#D0D0D0"}]
execute if score #lobAura lob matches 2 run data modify entity @e[tag=rlk_lk33,limit=1] text set value [{"text": "물", "color": "#3DA5FF"}, {"text": " (2초마다)", "color": "#D0D0D0"}]
execute if score #lobAura lob matches 3 run data modify entity @e[tag=rlk_lk33,limit=1] text set value [{"text": "번개", "color": "#B57BFF"}, {"text": " (2초마다)", "color": "#D0D0D0"}]
execute if score #lobAura lob matches 4 run data modify entity @e[tag=rlk_lk33,limit=1] text set value [{"text": "얼음", "color": "#9FEFFF"}, {"text": " (2초마다)", "color": "#D0D0D0"}]
execute if score #lobAura lob matches 5 run data modify entity @e[tag=rlk_lk33,limit=1] text set value [{"text": "풀", "color": "#7BD94A"}, {"text": " (2초마다)", "color": "#D0D0D0"}]
