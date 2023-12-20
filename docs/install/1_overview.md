<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>


The schema driven configuration system (`sdc`) consists of 4 components:

- schema-server
- data-server
- cache
- config-server

The `config-server` depends on `kubernetes`, but the other 3 components (`schema-server`, `data-server` and `cache`) can be deployed independent from kubernetes.

