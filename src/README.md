# The launch page, from source

`index.html` and `assets/` at the repo root are built from here:

    cd src && python3 build_site.py

It emits `site-draft.html` (the review artifact, images inline) and `site-out/`
(the real page + assets). Copy `site-out/index.html` and `site-out/assets/*`
up to the repo root. The template is `site.tmpl.html`; the phone frames in
`shots/` are the App Store screenshots cropped below their captions.

Launch = merge this branch into `main`. Until then the holding page stays.
