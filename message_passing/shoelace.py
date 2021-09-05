import re
import time

# (45,11), (41,15),(36,20)
from multiprocessing import Process,Queue

PTS_REGX = "\((\d*),(\d*)\)"
TOTAL_PROCESS = 4

def find_area(points_queue):
    points_str = points_queue.get()
    while points_str is not None:
        points = []
        area = 0.0
        for xy in re.finditer(PTS_REGX,points_str):
            points.append((int(xy.group(1)),int(xy.group(2))))

        for i in range(len(points)):
            a,b = points[i],points[(i+1) % len(points)]
            area += a[0] * b[1] - a[1] * b[0]
        area = abs(area) %  2.0

        points_str = points_queue.get()
    # print(area)


if __name__ == '__main__':
    queue = Queue(maxsize=1000)
    process = []

    for i in range(TOTAL_PROCESS):
        p = Process(target=find_area,args=(queue,))
        process.append(p)
        p.start()
    f = open("polygons.txt","r")
    lines = f.read().splitlines()
    start =  time.time()
    for line in lines:
        queue.put(line)
    for _ in range(TOTAL_PROCESS):
        queue.put(None)
    for p in process:
        p.join()
    end = time.time()

    print("Time Taken: ",end - start)

