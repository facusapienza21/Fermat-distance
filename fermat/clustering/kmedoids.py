from typing import List
import random
import numpy as np


def select_random_medoids(landmarks, k, seed):
    r = random.Random(seed) if seed else random.Random()
    return r.sample(landmarks, k)


def assign_closest_cluster_to_points(clusters, n):
    closest = [-1]*n
    distance_closest = [-1]*n
    for i, landmark in enumerate(clusters):
        for point in range(n):
            distance = landmark.root_distance(point)
            if distance < distance_closest[point] or closest[point] == -1:
                closest[point] = i
                distance_closest[point] = distance
    return closest


def assing_center_to_cluster(landmarks, centers, n, closest):

    clusters_distances = np.zeros((len(centers), len(landmarks)))

    for i, landmark in enumerate(landmarks):
        for point in range(n):
            clusters_distances[closest[point], i] += landmark.root_distance(point)

    distincts = list({np.argmin(d) for d in clusters_distances}) 
    return [landmarks[d] for d in distincts]


def do_k_medoids(landmarks, n: int, k: int, iterations: int, seed=None):
    
    centers = select_random_medoids(landmarks, k, seed)
    closest = assign_closest_cluster_to_points(centers, n)

    for _ in range(iterations):
        centers = assing_center_to_cluster(landmarks, centers, n, closest)
        closest = assign_closest_cluster_to_points(centers, n)
    
    return [centers[closest[i]].root for i in range(n)]