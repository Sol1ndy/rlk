# 아이템 레지스트리 초기화 및 등록 (load 에서 호출)
data modify storage rlk:items registry set value {}
data modify storage rlk:items ids set value []

# 등급 색 / 라벨 / 판매가 / 타입 라벨 매핑
data modify storage rlk:items rarity_color set value {character:"gold",common:"green",rare:"aqua",epic:"dark_purple",legendary:"yellow",mythic:"dark_red"}
data modify storage rlk:items rarity_label set value {character:"CHARACTER",common:"COMMON",rare:"RARE",epic:"UNIQUE",legendary:"LEGENDARY",mythic:"MYTHIC"}
data modify storage rlk:items rarity_kr set value {common:"일반",rare:"레어",epic:"유니크",legendary:"레전더리",mythic:"신화"}
data modify storage rlk:items rarity_price set value {character:200,common:352,rare:422,epic:562,legendary:842,mythic:1500}
data modify storage rlk:items type_label set value {character:"CHARACTER",weapon:"WEAPON",accessory:"ACCESSORY",armor:"ARMOR"}

# 아이템 모델: 1b 면 리소스팩의 rlk:<아이템id> 모델 사용, 0b(기본) 면 바닐라 아이템 모양 그대로
# 켜기: /data modify storage rlk:config use_models set value 1b  (아이템 정의에 model:"..." 을 넣으면 그 아이템은 항상 그 모델 사용)
execute unless data storage rlk:config use_models run data modify storage rlk:config use_models set value 0b

# ===== 아이템 정의 =====
# 새 아이템: items/<등급>/<id>/def.mcfunction 을 만들고 아래에 한 줄 추가. 보유 개수는 it_<id> 스코어로 자동 집계됨
function rlk:items/common/whetstone/def
function rlk:items/common/leather_armor/def
function rlk:items/common/traveler_boots/def
function rlk:items/common/seer_crystal/def
function rlk:items/common/squire_badge/def
function rlk:items/common/hourglass_shard/def
function rlk:items/common/coin_pouch/def
function rlk:items/common/red_herb/def
function rlk:items/common/dull_dagger/def
function rlk:items/common/hood/def
function rlk:items/common/cracked_lens/def
function rlk:items/common/old_gold_ring/def
function rlk:items/common/dried_fish/def
function rlk:items/common/obsidian_shard/def
function rlk:items/common/ember_matchbox/def
function rlk:items/common/dew_vial/def
function rlk:items/common/static_fur/def
function rlk:items/common/icicle/def
function rlk:items/common/pebble/def
function rlk:items/common/pinwheel/def
function rlk:items/common/sprout/def
function rlk:items/common/lucky_coin/def
function rlk:items/common/prayer_beads/def
function rlk:items/common/cavalry_coin/def
function rlk:items/common/witch_thimble/def
function rlk:items/common/captain_bracer/def
function rlk:items/common/contract_ink/def
function rlk:items/rare/favonius_codex/def
function rlk:items/rare/general_banner/def
function rlk:items/rare/hound_whistle/def
function rlk:items/rare/grass_ring/def
function rlk:items/rare/hurricane_core/def
function rlk:items/rare/musketeer_badge/def
function rlk:items/rare/rain_sheath/def
function rlk:items/rare/raven_feather/def
function rlk:items/rare/hot_pot/def
function rlk:items/rare/banner/def
function rlk:items/rare/baron_bunny/def
function rlk:items/rare/hunter_mark/def
function rlk:items/rare/thief_gloves/def
function rlk:items/rare/old_slate/def
function rlk:items/rare/tengu_feather/def
function rlk:items/rare/opera_flag/def
function rlk:items/rare/blazing_barrier/def
function rlk:items/rare/night_stars/def
function rlk:items/rare/genie_lamp/def
function rlk:items/rare/kinetic_scale/def
function rlk:items/rare/nightsoul_orb/def
function rlk:items/rare/wind_slime/def
function rlk:items/rare/maid_gauntlet/def
function rlk:items/rare/cat_cocktail/def
function rlk:items/rare/exorcist_charm/def
function rlk:items/rare/sinner_spear/def
function rlk:items/rare/pact_dagger/def
function rlk:items/rare/holy_shield/def
function rlk:items/epic/sealed_sword/def
function rlk:items/epic/lifeline/def
function rlk:items/epic/forbidden_book/def
function rlk:items/epic/maple_leaf/def
function rlk:items/epic/ice_quill/def
function rlk:items/epic/talisman/def
function rlk:items/epic/sun_blossom/def
function rlk:items/epic/jellyfish/def
function rlk:items/epic/obsidian_mirror/def
function rlk:items/epic/tailor_doll/def
function rlk:items/epic/star_wisp/def
function rlk:items/epic/astral_omen/def
function rlk:items/epic/lumidouce_case/def
function rlk:items/epic/seamless_shield/def
function rlk:items/epic/dragon_flame/def
function rlk:items/epic/dandelion_seed/def
function rlk:items/epic/crane_feather/def
function rlk:items/epic/nurse_syringe/def
function rlk:items/epic/chef_knife/def
function rlk:items/epic/harmonic_score/def
function rlk:items/epic/dream_pillow/def
function rlk:items/legendary/sword_kirion/def
function rlk:items/legendary/demonomicon/def
function rlk:items/legendary/pain_despair/def
function rlk:items/legendary/sesshou_sakura/def
function rlk:items/legendary/source_samples/def
function rlk:items/legendary/moonlit_loom/def
function rlk:items/legendary/mech_heart/def
function rlk:items/legendary/life_gourd/def
function rlk:items/legendary/lion_mane/def
function rlk:items/legendary/crimson_moon/def
function rlk:items/legendary/water_lily/def
function rlk:items/mythic/stormy_eye/def
function rlk:items/mythic/skyward_verse/def
function rlk:items/mythic/jade_shard/def
function rlk:items/mythic/skandha_seed/def
function rlk:items/mythic/salon_invite/def
function rlk:items/mythic/ember_oath/def
function rlk:items/mythic/moon_chalice/def
function rlk:items/engr_assign

# 등급순 정렬 + 등급별 목록(상점 추첨용) + 보유 개수 스코어(it_<id>) 생성
function rlk:items/sort_by_rarity
function rlk:items/build_rarbuckets
data modify storage rlk:items fscan set from storage rlk:items ids
function rlk:items/reg_flags_loop
# 능력 구현 완료 아이템 목록(items/debug 에서 미구현=빨강 표시용). 새 아이템 구현 시 여기에 id 추가
data modify storage rlk:items impl set value ["sealed_sword","sword_kirion","forbidden_book","demonomicon","pain_despair","stormy_eye","favonius_codex","whetstone","leather_armor","traveler_boots","seer_crystal","squire_badge","hourglass_shard","coin_pouch","red_herb","dull_dagger","hood","rain_sheath","raven_feather","hot_pot","banner","maple_leaf","jade_shard","ice_quill","baron_bunny","talisman","sun_blossom","hunter_mark","thief_gloves","old_slate","cracked_lens","old_gold_ring","dried_fish","obsidian_shard","ember_matchbox","dew_vial","static_fur","icicle","pebble","pinwheel","sprout","jellyfish","general_banner","skandha_seed","obsidian_mirror","tailor_doll","moon_chalice","star_wisp","hound_whistle","grass_ring","hurricane_core","musketeer_badge","salon_invite","sesshou_sakura","source_samples","ember_oath","lifeline","skyward_verse","astral_omen","lumidouce_case","seamless_shield","dragon_flame","tengu_feather","opera_flag","blazing_barrier","night_stars","genie_lamp","kinetic_scale","nightsoul_orb","wind_slime","lucky_coin","prayer_beads","cavalry_coin","witch_thimble","captain_bracer","contract_ink","maid_gauntlet","cat_cocktail","exorcist_charm","sinner_spear","pact_dagger","holy_shield","dandelion_seed","crane_feather","nurse_syringe","chef_knife","harmonic_score","dream_pillow","moonlit_loom","mech_heart","life_gourd","lion_mane","crimson_moon","water_lily"]
# 챕터별 등급 확률 (누적 천분율: t1 = 일반, t2 = +레어, t3 = +유니크, t4 = +레전더리, 나머지 = 신화). 6챕터 이후는 c6 을 씀
#   1챕터: 일반 60.0% / 레어 33.0% / 유니크 7.0% / 레전더리 0.0% / 신화 0.0%
#   3챕터: 일반 38.0% / 레어 37.0% / 유니크 20.0% / 레전더리 4.5% / 신화 0.5%
#   6챕터: 일반 13.0% / 레어 29.0% / 유니크 36.0% / 레전더리 17.0% / 신화 5.0%
data modify storage rlk:items rar_wt set value {c1:{t1:600,t2:930,t3:1000,t4:1000},c2:{t1:480,t2:840,t3:980,t4:1000},c3:{t1:380,t2:750,t3:950,t4:995},c4:{t1:280,t2:640,t3:910,t4:985},c5:{t1:200,t2:530,t3:850,t4:970},c6:{t1:130,t2:420,t3:780,t4:950}}
