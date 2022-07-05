#!/bin/sh

# see https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/style-src#unsafe_inline_styles
# save as .htaccess

extract() {
	open=0
	while IFS= read -r line; do
		if [ "$line" = "	<$1>" ]; then
			open=1
			printf "\n"
		elif [ "$line" = "	</$1>" ]; then
			open=0
			printf "	"
		elif [ "$open" = 1 ]; then
			echo "$line"
		fi
	done < template.html
}

stylesrc=$(extract 'style' | openssl dgst -sha256 -binary | openssl enc -base64)
scriptsrc=$(extract 'script' | openssl dgst -sha256 -binary | openssl enc -base64)

echo '<Files "*.*">'
echo "Header set Content-Security-Policy \"default-src 'self'; style-src 'sha256-$stylesrc'; script-src 'sha256-$scriptsrc'\""
echo '</Files>'
