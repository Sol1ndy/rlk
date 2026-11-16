# Put-away clip "sheathe" (Skirk), started by char/motion/sheath/begin when the drawn delay runs out while idle
# on the ground. No gameplay events and no movement lock: attacks draw instantly and movement aborts it.
# The weapon_attach "back" frame (tick 48) sets pmSheath 1 through the generated sheath/clip_state.
# Sound layers: tools/player_motion/audio_skirk.py ("sheathe"), compiled by tools/build_player_audio.py.
function rlk:char/motion/audio/skirk/sheathe
