
workflow: raw-emojis.json emojilib.json codes.json
	rm -rf icons/
	python3 make_workflow.py

emojilib.json:
	curl https://raw.githubusercontent.com/muan/emojilib/master/emojis.json > emojilib.json

raw-emojis.json: full-emoji-list.html
	python3 parse_html.py

full-emoji-list.html:
	curl https://unicode.org/emoji/charts/full-emoji-list.html > full-emoji-list.html

