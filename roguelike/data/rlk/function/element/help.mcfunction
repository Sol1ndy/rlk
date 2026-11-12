# element/infuse · infuse_for · give {id:"help"} (macro: cmd = 명령 모양, pre · post = 채울 명령 앞뒤): rlk:elem ids 의 대표 이름과
# 한글 이름 (byid.<id>.name, element/setup). 한글 · 원신식 별명은 byid 에 있다
$function rlk:help/head {cmd:"$(cmd)",what:"원소 id"}
$data modify storage rlk:help r set value {pre:'$(pre)',post:'$(post)',st:"rlk:elem",np:"byid.",ns:".name"}
data modify storage rlk:help q set from storage rlk:elem ids
function rlk:help/list
tellraw @s ["",{text:" 한글 이름(불 · 물 · 번개 · 얼음 · 바위 · 바람 · 풀 · 물리)과 원신식 이름(pyro · hydro · electro · cryo · geo · anemo · dendro)도 됩니다. physical = 해제",color:"gray"}]
data remove storage rlk:help r
