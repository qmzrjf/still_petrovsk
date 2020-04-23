 #!/bin/bash

rm /srv/project/run/celery.pid
celery -A still_petrovsk worker -l info --workdir=/srv/project/src --pidfile=/srv/project/run/celery.pid