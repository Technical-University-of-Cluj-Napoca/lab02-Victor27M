#!/usr/bin/env python3
import sys
from collections import deque

# --- ANSI palette (works in most terminals; on old Windows CMD colors may be ignored) ---
ANSI = {
    "reset": "\033[0m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "magenta": "\033[95m",
    "gray": "\033[90m",
}

# Solid block so the maze looks like squares
BLOCK = "█"


# -------------------- I/O --------------------
def read_maze(filename):
    """Return maze as list[list[str]] (rows), without trailing newlines."""
    maze = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            maze.append(list(line.rstrip("\n")))
    return maze


def find_start_and_target(maze):
    """Return (start_row, start_col), (target_row, target_col)."""
    start = target = None
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
            elif ch == "T":
                target = (r, c)
            if start and target:
                return start, target
    raise ValueError("Maze must contain both 'S' and 'T'.")


# -------------------- Graph helpers --------------------
def get_neighbors(maze, pos):
    """4-neighbors that are in-bounds and not walls (#)."""
    r, c = pos
    H, W = len(maze), len(maze[0])
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < H and 0 <= nc < W and maze[nr][nc] != "#":
            yield (nr, nc)


# -------------------- Searches --------------------
def bfs(maze, start, target):
    """Breadth-First Search — returns shortest path as a list of positions."""
    q = deque([start])
    parent = {start: None}
    while q:
        cur = q.popleft()
        if cur == target:
            break
        for nb in get_neighbors(maze, cur):
            if nb not in parent:
                parent[nb] = cur
                q.append(nb)

    if target not in parent:
        return []
    # reconstruct
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


def dfs(maze, start, target):
    """
    DFS with backtracking that keeps the *shortest* path found.
    (So behavior matches the lab code you shared.)
    """
    best_path = []
    visited = set()

    def backtrack(cur, path):
        nonlocal best_path
        # prune if current path already longer than best
        if best_path and len(path) >= len(best_path):
            return
        if cur == target:
            if not best_path or len(path) < len(best_path):
                best_path = path[:]
            return
        visited.add(cur)
        for nb in get_neighbors(maze, cur):
            if nb not in visited:
                path.append(nb)
                backtrack(nb, path)
                path.pop()
        visited.remove(cur)

    backtrack(start, [start])
    return best_path


# -------------------- Printing --------------------
def print_maze_with_path(maze, path, color="green"):
    """Pretty print maze using colored full blocks for walls/path/start/target."""
    col = ANSI.get(color, ANSI["green"])
    reset = ANSI["reset"]
    path_set = set(path)

    # copy so we don't mutate original
    grid = [row[:] for row in maze]
    for (r, c) in path_set:
        if grid[r][c] not in ("S", "T", "#"):
            grid[r][c] = "."

    for r, row in enumerate(grid):
        out = []
        for c, ch in enumerate(row):
            if ch == "#":
                out.append(f"{ANSI['gray']}{BLOCK}{reset}")
            elif (r, c) in path_set and ch == ".":
                out.append(f"{col}{BLOCK}{reset}")
            elif ch == "S":
                out.append(f"{ANSI['yellow']}{BLOCK}{reset}")
            elif ch == "T":
                out.append(f"{ANSI['magenta']}{BLOCK}{reset}")
            else:
                out.append(" ")
        print("".join(out))


# -------------------- Main --------------------
def main():
    if len(sys.argv) != 3:
        print("Usage: python search_maze.py <bfs|dfs> <maze_file>")
        sys.exit(1)

    method = sys.argv[1].lower()
    maze_file = sys.argv[2]

    maze = read_maze(maze_file)
    start, target = find_start_and_target(maze)

    if method == "bfs":
        path = bfs(maze, start, target)
        color = "green"
    elif method == "dfs":
        path = dfs(maze, start, target)
        color = "red"
    else:
        print("Unknown method. Use 'bfs' or 'dfs'.")
        sys.exit(1)

    print("\nMaze with path:")
    if path:
        print_maze_with_path(maze, path, color=color)
    else:
        print("No path found.")


if __name__ == "__main__":
    main()
