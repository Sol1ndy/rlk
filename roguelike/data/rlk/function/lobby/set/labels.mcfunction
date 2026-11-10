# 설정 오브젝트 이름표에 지금 값
function rlk:lobby/set/cfg
execute if data storage rlk:lobby cfg{dist:0} run data modify entity @e[tag=rlk_lk21,limit=1] text set value {"text": "가까이", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{dist:1} run data modify entity @e[tag=rlk_lk21,limit=1] text set value {"text": "보통", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{dist:2} run data modify entity @e[tag=rlk_lk21,limit=1] text set value {"text": "멀리", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{h:0} run data modify entity @e[tag=rlk_lk23,limit=1] text set value {"text": "낮게", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{h:1} run data modify entity @e[tag=rlk_lk23,limit=1] text set value {"text": "보통", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{h:2} run data modify entity @e[tag=rlk_lk23,limit=1] text set value {"text": "높게", "color": "#D0D0D0"}
data modify entity @e[tag=rlk_lk26,limit=1] text set value {"text": "1개 (사파이어로 해금 예정)", "color": "#D0D0D0"}
