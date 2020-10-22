#!/bin/sh
# Keep calling the sample tool to keep the logs following in

set -e

while true; do
    numbers=$(python -c "import random; print(' '.join(str(random.randint(1, 9999)) for _ in range(20)))")
    parallel=$(python -c "import random; print('--parallel' if random.randint(0, 1) else '')")
    st work $numbers -l 1 $parallel 
    sleep $(python -c "import random; print(random.randint(0, 10))")
done
