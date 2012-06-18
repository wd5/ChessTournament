#!/bin/bash

lessc styles/style.less > static/css/style.css

echo '' > static/js/bootstrap.js
cat styles/bootstrap/js/bootstrap-transition.js >> static/js/bootstrap.js
cat styles/bootstrap/js/bootstrap-collapse.js >> static/js/bootstrap.js
cat styles/bootstrap/js/bootstrap-modal.js >> static/js/bootstrap.js