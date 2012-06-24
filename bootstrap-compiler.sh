#!/bin/bash

lessc styles/style.less > static/css/style.css

echo '' > static/js/jquery.bootstrap.js
cat styles/bootstrap/js/bootstrap-transition.js >> static/js/jquery.bootstrap.js
cat styles/bootstrap/js/bootstrap-collapse.js >> static/js/jquery.bootstrap.js
cat styles/bootstrap/js/bootstrap-modal.js >> static/js/jquery.bootstrap.js
cat styles/bootstrap/js/bootstrap-alert.js >> static/js/jquery.bootstrap.js
cat styles/bootstrap/js/bootstrap-dropdown.js >> static/js/jquery.bootstrap.js