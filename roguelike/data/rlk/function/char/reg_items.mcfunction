# 캐릭터 아이템 등록 (load 에서 items/register 뒤에 호출). 새 캐릭터를 만들면 여기에 한 줄 + rlk:chars pool 에 추가
#   pool = 선택지로 나올 수 있는 캐릭터 목록(루미네는 시작 캐릭터라 넣지 않음. 바닥에 내려놓은 루미네는 다시 주울 수 있다)
data modify storage rlk:chars pool set value [{id:"yoimiya",item:"char_yoimiya"}]
function rlk:char/reg_item with storage rlk:chars registry.lumine
function rlk:char/reg_item with storage rlk:chars registry.yoimiya
function rlk:char/reg_item with storage rlk:chars registry.skirk
data modify storage rlk:chars pool append value {id:"skirk",item:"char_skirk"}
# 도감의 캐릭터 탭
data modify storage rlk:codex chars set value ["char_lumine","char_yoimiya","char_skirk"]
function rlk:char/reg_item with storage rlk:chars registry.clorinde
data modify storage rlk:chars pool append value {id:"clorinde",item:"char_clorinde"}
data modify storage rlk:codex chars append value "char_clorinde"
function rlk:char/reg_item with storage rlk:chars registry.arlecchino
data modify storage rlk:chars pool append value {id:"arlecchino",item:"char_arlecchino"}
data modify storage rlk:codex chars append value "char_arlecchino"
function rlk:char/reg_item with storage rlk:chars registry.navia
data modify storage rlk:chars pool append value {id:"navia",item:"char_navia"}
data modify storage rlk:codex chars append value "char_navia"
function rlk:char/reg_item with storage rlk:chars registry.ronova
# 로노바: 레벨 업 선택지에는 나오지 않는다(따로 얻는 캐릭터)
data modify storage rlk:codex chars append value "char_ronova"
function rlk:char/reg_item with storage rlk:chars registry.nefer
data modify storage rlk:chars pool append value {id:"nefer",item:"char_nefer"}
data modify storage rlk:codex chars append value "char_nefer"
