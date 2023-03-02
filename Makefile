
all: Emoji.alfredworkflow

Emoji.alfredworkflow: alfred-emoji.json icons/
	zip Emoji.alfredworkflow -r \
		icons/ \
		info.plist \
		icon.png \
		alfred-emoji.json \
		README.md

alfred-emoji.json: raw-emojis.json emojilib.json unicode-emoji.json codes.json
	rm -rf icons/
	python3 make_workflow.py

emojilib.json:
	curl https://raw.githubusercontent.com/muan/emojilib/main/dist/emoji-en-US.json > $@

unicode-emoji.json:
	curl https://raw.githubusercontent.com/muan/unicode-emoji-json/main/data-by-emoji.json > $@

raw-emojis.json: full-emoji-list.html
	python3 parse_html.py

full-emoji-list.html:
	curl https://unicode.org/emoji/charts/full-emoji-list.html > $@

clean: Emoji.alfredworkflow emojilib.json unicode-emoji.json raw-emojis.json full-emoji-list.html
.PHONY: all clean
