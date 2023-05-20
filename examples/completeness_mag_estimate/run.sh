#/bin/sh

# etas-mc {magnitudes file} -min {minimum test mc} -max {maximum test mc} -d {mc test interval} -p {significance value} -n {number of samples}
etas-mc magnitudes.npy -min 2 -max 5.5 -d 0.1 -p 0.05 -n 1000
