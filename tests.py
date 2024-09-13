from memsim import Memsim

files = ["bzip.trace", "gcc.trace", "swim.trace", "sixpack.trace"]
algs = ["rand", "lru", "clock"]
frame_counts = [3000, 2000, 1000, 500, 200, 100, 50, 40, 30, 20, 15, 10, 5, 3, 2, 1]
memsim = Memsim()

for file in files:
    with open(file, "r") as f:
        lines = f.readlines()
        temp = open(file+".csv", "w")
        temp.close()
        with open(file+".csv", "a") as f2:
            for alg in algs:
                f2.write(f"Algorithm: {alg}\n")
                for frame_count in frame_counts:
                    print(f"Running {file} with {alg} and {frame_count} frames")
                    return_vals = Memsim.run(file, frame_count, alg)
                    f2.write(str(return_vals[0]) + "," + str(return_vals[1]) + "," + str(return_vals[2]) + "," + str(return_vals[3]) + "," + str(return_vals[4]) + "\n")

