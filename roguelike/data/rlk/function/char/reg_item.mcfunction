# macro: id (캐릭터 등록 내용 전체가 들어온다). 설명 = 캐릭터 정보(info.lore), 모양 = 그 캐릭터 스킨의 머리
$data modify storage rlk:items registry.char_$(id) set value {item:"minecraft:player_head",type:"character",rarity:"character",stats:{},desc:[],char:"$(id)"}
$data modify storage rlk:items registry.char_$(id).name set from storage rlk:chars registry.$(id).info.name
$data modify storage rlk:items registry.char_$(id).abilities set from storage rlk:chars registry.$(id).info.lore
$data modify storage rlk:items registry.char_$(id).prof set from storage rlk:chars registry.$(id).info.prof
# 레벨 업 · 도감의 캐릭터 설명에는 고유 특성도 이어 붙인다
$execute if data storage rlk:chars registry.$(id).info.passive[0] run data modify storage rlk:items registry.char_$(id).abilities append value {text:"",italic:false}
$data modify storage rlk:items registry.char_$(id).abilities append from storage rlk:chars registry.$(id).info.passive[]
