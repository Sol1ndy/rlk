# 캐릭터 등록 (load 에서 호출). 새 캐릭터 = char/<id>/def 를 만들고 여기에 한 줄 추가 + char/cast_* · char/tick 의 분기에 번호 추가
# 무기 타입(weaponType): sword(한손검) / bow(활) / catalyst(법구) — 한손검·활이 구현되어 있음(활 = char/bow/*)
data modify storage rlk:chars registry set value {}
function rlk:char/lumine/def
function rlk:char/yoimiya/def
function rlk:char/skirk/def
function rlk:char/clorinde/def
function rlk:char/arlecchino/def
function rlk:char/navia/def
function rlk:char/ronova/def
function rlk:char/nefer/def
# 선택된 캐릭터가 있으면 등록 내용으로 갱신, 없으면 기본 캐릭터(루미네)
execute unless data storage rlk:chars cur.id run data modify storage rlk:chars cur set value {id:"lumine"}
function rlk:char/load_cur with storage rlk:chars cur
# 시작 캐릭터(런 시작·실패·리셋 때 이 캐릭터로 돌아간다). 바꾸려면: /data modify storage rlk:config start_char set value "yoimiya"
execute unless data storage rlk:config start_char run data modify storage rlk:config start_char set value "lumine"
