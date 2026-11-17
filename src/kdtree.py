import heapq
from src.hospital import dist2

class Node:

    def __init__(self, hospital, axis, left, right):
        self.hospital = hospital
        self.axis = axis
        self.left = left
        self.right = right

def build(hospitals, depth = 0):
    if not hospitals:
        return None

    axis = depth % 2

    if axis == 0:
        ordered = sorted(hospitals, key=lambda h: h.x)
    else:
        ordered = sorted(hospitals, key=lambda h: h.y)

    mid = len(ordered) // 2
    return Node(
        hospital = ordered[mid],
        axis = axis,
        left = build(ordered[:mid], depth + 1),
        right = build(ordered[mid + 1:], depth + 1),
    )

def nearest_k(root, qx, qy, k, accept=None):
    heap = []
    _search(root, qx, qy, k, heap, accept)

    result = [(-neg_d, h) for neg_d, neg_id, h in heap]
    result.sort(key=lambda pair:(pair[0], pair[1].id))
    return result

def _search(node, qx, qy, k, heap, accept):
    if node is None:
        return

    h = node.hospital

    if accept is None or accept(h):
        d2 = dist2(h, qx, qy)
        if len(heap) < k:
            heapq.heappush(heap, (-d2, -h.id, h))
        elif d2 < -heap[0][0]:
            heapq.heapreplace(heap, (-d2, -h.id, h))

    if node.axis == 0:
        diff = qx - h.x
    else:
        diff = qy - h.y

    if diff < 0:
        near, far = node.left, node.right
    else:
        near, far = node.right, node.left

    _search(near, qx, qy, k, heap, accept)

    if len(heap) < k or diff * diff < -heap[0][0]:
        _search(far, qx, qy, k ,heap, accept)