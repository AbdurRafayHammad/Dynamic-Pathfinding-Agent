import tkinter as tk
import tkinter.messagebox
import heapq
import math
import time
import random

BG = "#0f0f0f"
PANEL = "#141414"
BORDER = "#222222"
EMPTY = "#1a1a1a"
WALL = "#3a3a3a"
GREEN = "#00c896"
RED = "#ff4f5e"
BLUE = "#2a52a8"
PURPLE = "#c084fc"
CYAN = "#00e5ff"
WHITE = "#ffffff"
TEXT = "#e0e0e0"
MUTED = "#666666"

EMPTY_CELL = 0
WALL_CELL = 1
START_CELL = 2
GOAL_CELL = 3

WALL_MODE = "wall"
ERASE_MODE = "erase"
START_MODE = "start"
GOAL_MODE = "goal"

DEFAULT_ROWS = 20
DEFAULT_COLS = 20
DEFAULT_DENSITY = 0.30
CELL_PX = 24
ANIM_MS = 80
SPAWN_CHANCE = 0.12


def manhattan(a, b):
    row_diff = abs(a[0] - b[0])
    col_diff = abs(a[1] - b[1])
    return row_diff + col_diff


def euclidean(a, b):
    row_diff = a[0] - b[0]
    col_diff = a[1] - b[1]
    return math.sqrt(row_diff ** 2 + col_diff ** 2)


def new_grid(rows, cols):
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(EMPTY_CELL)
        grid.append(row)
    return grid


def get_neighbors(grid, rows, cols, r, c):
    result = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr = r + dr
        nc = c + dc
        in_bounds = 0 <= nr < rows and 0 <= nc < cols
        if in_bounds and grid[nr][nc] != WALL_CELL:
            result.append((nr, nc))
    return result


def build_path(came_from, start, goal):
    path = []
    node = goal
    while node in came_from:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    return path


def astar(grid, rows, cols, start, goal, hfn):
    open_list = []
    heapq.heappush(open_list, (0, 0, start))

    came_from = {}
    g_cost = {}
    g_cost[start] = 0
    expanded = set()

    while open_list:
        f, g, current = heapq.heappop(open_list)

        if current in expanded:
            continue

        expanded.add(current)

        if current == goal:
            path = build_path(came_from, start, goal)
            return path, expanded, g_cost[goal]

        neighbors = get_neighbors(grid, rows, cols, current[0], current[1])

        for neighbor in neighbors:
            new_g = g_cost[current] + 1

            old_g = g_cost.get(neighbor, float("inf"))

            if new_g < old_g:
                g_cost[neighbor] = new_g
                came_from[neighbor] = current
                h = hfn(neighbor, goal)
                f_val = new_g + h
                heapq.heappush(open_list, (f_val, new_g, neighbor))

    return [], expanded, 0


def gbfs(grid, rows, cols, start, goal, hfn):
    open_list = []
    heapq.heappush(open_list, (hfn(start, goal), start))

    came_from = {}
    visited = set()
    visited.add(start)
    expanded = set()

    while open_list:
        h, current = heapq.heappop(open_list)
        expanded.add(current)

        if current == goal:
            path = build_path(came_from, start, goal)
            cost = len(path) - 1
            return path, expanded, cost

        neighbors = get_neighbors(grid, rows, cols, current[0], current[1])

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                h_val = hfn(neighbor, goal)
                heapq.heappush(open_list, (h_val, neighbor))

    return [], expanded, 0


def run_search(algo, heur, grid, rows, cols, start, goal):
    if heur == "Manhattan":
        hfn = manhattan
    else:
        hfn = euclidean

    t0 = time.perf_counter()

    if algo == "A*":
        path, expanded, cost = astar(grid, rows, cols, start, goal, hfn)
    else:
        path, expanded, cost = gbfs(grid, rows, cols, start, goal, hfn)

    t1 = time.perf_counter()
    ms = round((t1 - t0) * 1000, 2)

    return path, expanded, cost, ms


class GridSizeDialog(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Grid Setup")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self.result = None

        tk.Label(self, text="Set Grid Size", bg=BG, fg=WHITE, font=("Consolas", 12, "bold")).pack(pady=(16, 8))

        form = tk.Frame(self, bg=BG)
        form.pack(padx=24, pady=4)

        tk.Label(form, text="Rows (5-40):", bg=BG, fg=TEXT, font=("Consolas", 9)).grid(row=0, column=0, sticky="w", pady=4)

        self.rows_var = tk.IntVar(value=DEFAULT_ROWS)
        tk.Spinbox(form, from_=5, to=40, textvariable=self.rows_var, width=6, font=("Consolas", 9), bg=PANEL, fg=TEXT, buttonbackground=BORDER, relief=tk.FLAT).grid(row=0, column=1, padx=8)

        tk.Label(form, text="Cols (5-40):", bg=BG, fg=TEXT, font=("Consolas", 9)).grid(row=1, column=0, sticky="w", pady=4)

        self.cols_var = tk.IntVar(value=DEFAULT_COLS)
        tk.Spinbox(form, from_=5, to=40, textvariable=self.cols_var, width=6, font=("Consolas", 9), bg=PANEL, fg=TEXT, buttonbackground=BORDER, relief=tk.FLAT).grid(row=1, column=1, padx=8)

        tk.Button(self, text="Start", command=self.confirm, bg=GREEN, fg=BG, font=("Consolas", 10, "bold"), relief=tk.FLAT, padx=20, pady=6, cursor="hand2").pack(pady=16)

        self.protocol("WM_DELETE_WINDOW", self.confirm)
        self.wait_window()

    def confirm(self):
        self.result = (self.rows_var.get(), self.cols_var.get())
        self.destroy()


class App:

    def __init__(self, root, rows, cols):
        self.root = root
        self.root.title("Pathfinding Agent")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.rows = rows
        self.cols = cols

        self.grid = new_grid(rows, cols)

        self.start = (1, 1)
        self.goal = (rows - 2, cols - 2)

        self.grid[self.start[0]][self.start[1]] = START_CELL
        self.grid[self.goal[0]][self.goal[1]] = GOAL_CELL

        self.algo = tk.StringVar(value="A*")
        self.heur = tk.StringVar(value="Manhattan")
        self.dynamic = tk.BooleanVar(value=False)
        self.draw_mode = WALL_MODE

        self.path_set = set()
        self.visited_set = set()
        self.path_list = []
        self.agent_pos = None
        self.agent_idx = 0
        self.running = False

        self.nodes_var = tk.StringVar(value="—")
        self.cost_var = tk.StringVar(value="—")
        self.time_var = tk.StringVar(value="—")

        self.build_topbar()
        self.build_body()
        self.build_metrics()
        self.redraw()

    def build_topbar(self):
        top = tk.Frame(self.root, bg=BG, pady=8)
        top.pack(fill=tk.X)

        tk.Label(top, text="PATHFINDING AGENT", bg=BG, fg=WHITE, font=("Consolas", 13, "bold")).pack(side=tk.LEFT, padx=16)

        right = tk.Frame(top, bg=BG)
        right.pack(side=tk.RIGHT, padx=16)

        self.make_pill_row(right, self.algo, ["A*", "GBFS"])

        tk.Frame(right, bg=BG, width=10).pack(side=tk.LEFT)

        self.make_pill_row(right, self.heur, ["Manhattan", "Euclidean"])

        tk.Frame(right, bg=BG, width=10).pack(side=tk.LEFT)

        tk.Checkbutton(right, text="Dynamic", variable=self.dynamic, bg=BG, fg=MUTED, selectcolor=BG, activebackground=BG, activeforeground=TEXT, font=("Consolas", 8), indicatoron=False, relief=tk.FLAT, padx=8, pady=4, cursor="hand2").pack(side=tk.LEFT)

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill=tk.X)

    def make_pill_row(self, parent, var, options):
        frame = tk.Frame(parent, bg=BORDER)
        frame.pack(side=tk.LEFT)
        for opt in options:
            tk.Radiobutton(frame, text=opt, variable=var, value=opt, bg=BG, fg=MUTED, selectcolor=PANEL, activebackground=BG, activeforeground=TEXT, font=("Consolas", 8), indicatoron=False, relief=tk.FLAT, padx=8, pady=4, cursor="hand2").pack(side=tk.LEFT)

    def build_body(self):
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill=tk.BOTH, expand=True)

        sidebar = tk.Frame(body, bg=PANEL, width=160, padx=12, pady=12)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        self.build_sidebar(sidebar)

        wrap = tk.Frame(body, bg=BG, padx=12, pady=12)
        wrap.pack(side=tk.LEFT)

        w = self.cols * CELL_PX
        h = self.rows * CELL_PX

        self.canvas = tk.Canvas(wrap, width=w, height=h, bg=EMPTY, highlightthickness=1, highlightbackground=BORDER)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def build_sidebar(self, parent):
        tk.Label(parent, text="DRAW MODE", bg=PANEL, fg=MUTED, font=("Consolas", 7)).pack(anchor="w", pady=(0, 4))

        modes = [("Wall", WALL_MODE), ("Erase", ERASE_MODE), ("Start", START_MODE), ("Goal", GOAL_MODE)]
        self.mode_btns = {}

        for label, mode in modes:
            if mode == WALL_MODE:
                btn_bg = GREEN
                btn_fg = BG
            else:
                btn_bg = BORDER
                btn_fg = TEXT
            btn = tk.Button(parent, text=label, bg=btn_bg, fg=btn_fg, font=("Consolas", 8), relief=tk.FLAT, padx=6, pady=4, cursor="hand2", activebackground=GREEN, activeforeground=BG, command=lambda m=mode: self.set_mode(m))
            btn.pack(fill=tk.X, pady=1)
            self.mode_btns[mode] = btn

        tk.Frame(parent, bg=BORDER, height=1).pack(fill=tk.X, pady=8)

        tk.Label(parent, text="MAP", bg=PANEL, fg=MUTED, font=("Consolas", 7)).pack(anchor="w", pady=(0, 4))

        tk.Button(parent, text="Generate Map", command=self.generate, bg=BORDER, fg=TEXT, font=("Consolas", 8), relief=tk.FLAT, padx=6, pady=4, cursor="hand2", activebackground=GREEN, activeforeground=BG).pack(fill=tk.X, pady=1)

        tk.Button(parent, text="Clear Walls", command=self.clear, bg=BORDER, fg=TEXT, font=("Consolas", 8), relief=tk.FLAT, padx=6, pady=4, cursor="hand2", activebackground=GREEN, activeforeground=BG).pack(fill=tk.X, pady=1)

        tk.Button(parent, text="Resize Grid", command=self.resize, bg=BORDER, fg=TEXT, font=("Consolas", 8), relief=tk.FLAT, padx=6, pady=4, cursor="hand2", activebackground=GREEN, activeforeground=BG).pack(fill=tk.X, pady=1)

        tk.Frame(parent, bg=BORDER, height=1).pack(fill=tk.X, pady=8)

        tk.Label(parent, text="SEARCH", bg=PANEL, fg=MUTED, font=("Consolas", 7)).pack(anchor="w", pady=(0, 4))

        tk.Button(parent, text="▶  RUN", command=self.run, bg=GREEN, fg=BG, font=("Consolas", 9, "bold"), relief=tk.FLAT, padx=6, pady=6, cursor="hand2", activebackground="#00a87e", activeforeground=BG).pack(fill=tk.X, pady=1)

        tk.Button(parent, text="⬛  STOP", command=self.stop, bg=BORDER, fg=RED, font=("Consolas", 9, "bold"), relief=tk.FLAT, padx=6, pady=6, cursor="hand2", activebackground="#300010", activeforeground=RED).pack(fill=tk.X, pady=1)

        tk.Frame(parent, bg=BORDER, height=1).pack(fill=tk.X, pady=8)

        tk.Label(parent, text="LEGEND", bg=PANEL, fg=MUTED, font=("Consolas", 7)).pack(anchor="w", pady=(0, 4))

        legend = [(GREEN, "Start"), (RED, "Goal"), (WALL, "Wall"), (BLUE, "Visited"), (PURPLE, "Path"), (CYAN, "Agent")]

        for color, name in legend:
            row = tk.Frame(parent, bg=PANEL)
            row.pack(anchor="w", pady=1)
            tk.Label(row, bg=color, width=2, height=1).pack(side=tk.LEFT, padx=(0, 5))
            tk.Label(row, text=name, bg=PANEL, fg=TEXT, font=("Consolas", 7)).pack(side=tk.LEFT)

    def build_metrics(self):
        bottom = tk.Frame(self.root, bg=BG, pady=6)
        bottom.pack(fill=tk.X)

        metrics = [("Nodes Visited", self.nodes_var), ("Path Cost", self.cost_var), ("Time (ms)", self.time_var)]

        for label, var in metrics:
            box = tk.Frame(bottom, bg=PANEL, padx=16, pady=6)
            box.pack(side=tk.LEFT, padx=10)
            tk.Label(box, text=label, bg=PANEL, fg=MUTED, font=("Consolas", 7)).pack()
            tk.Label(box, textvariable=var, bg=PANEL, fg=GREEN, font=("Consolas", 13, "bold")).pack()

    def set_mode(self, mode):
        self.draw_mode = mode
        for m, btn in self.mode_btns.items():
            if m == mode:
                btn.configure(bg=GREEN, fg=BG)
            else:
                btn.configure(bg=BORDER, fg=TEXT)

    def get_cell_color(self, r, c):
        v = self.grid[r][c]

        if v == START_CELL:
            return GREEN

        if v == GOAL_CELL:
            return RED

        if v == WALL_CELL:
            return WALL

        if self.agent_pos == (r, c):
            return CYAN

        if (r, c) in self.path_set:
            return PURPLE

        if (r, c) in self.visited_set:
            return BLUE

        return EMPTY

    def redraw(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_PX
                y1 = r * CELL_PX
                x2 = x1 + CELL_PX
                y2 = y1 + CELL_PX
                color = self.get_cell_color(r, c)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=BG, width=1)

    def to_cell(self, event):
        r = event.y // CELL_PX
        c = event.x // CELL_PX
        return r, c

    def draw_at(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return

        protected = self.grid[r][c] == START_CELL or self.grid[r][c] == GOAL_CELL

        if self.draw_mode == WALL_MODE and not protected:
            self.grid[r][c] = WALL_CELL

        elif self.draw_mode == ERASE_MODE and not protected:
            self.grid[r][c] = EMPTY_CELL

        elif self.draw_mode == START_MODE:
            self.grid[self.start[0]][self.start[1]] = EMPTY_CELL
            self.start = (r, c)
            self.grid[r][c] = START_CELL

        elif self.draw_mode == GOAL_MODE:
            self.grid[self.goal[0]][self.goal[1]] = EMPTY_CELL
            self.goal = (r, c)
            self.grid[r][c] = GOAL_CELL

        self.redraw()

    def on_click(self, event):
        if not self.running:
            r, c = self.to_cell(event)
            self.draw_at(r, c)

    def on_drag(self, event):
        if not self.running:
            r, c = self.to_cell(event)
            self.draw_at(r, c)

    def generate(self):
        self.stop()
        self.reset_viz()
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == self.start or (r, c) == self.goal:
                    continue
                if random.random() < DEFAULT_DENSITY:
                    self.grid[r][c] = WALL_CELL
                else:
                    self.grid[r][c] = EMPTY_CELL
        self.redraw()

    def clear(self):
        self.stop()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == WALL_CELL:
                    self.grid[r][c] = EMPTY_CELL
        self.reset_viz()
        self.redraw()

    def resize(self):
        self.stop()
        dialog = GridSizeDialog(self.root)
        if dialog.result is None:
            return
        new_rows = dialog.result[0]
        new_cols = dialog.result[1]
        self.rows = new_rows
        self.cols = new_cols
        self.grid = new_grid(new_rows, new_cols)
        self.start = (1, 1)
        self.goal = (new_rows - 2, new_cols - 2)
        self.grid[self.start[0]][self.start[1]] = START_CELL
        self.grid[self.goal[0]][self.goal[1]] = GOAL_CELL
        self.canvas.configure(width=new_cols * CELL_PX, height=new_rows * CELL_PX)
        self.reset_viz()
        self.redraw()

    def reset_viz(self):
        self.path_set = set()
        self.visited_set = set()
        self.path_list = []
        self.agent_pos = None
        self.agent_idx = 0
        self.running = False
        self.nodes_var.set("—")
        self.cost_var.set("—")
        self.time_var.set("—")

    def stop(self):
        self.running = False

    def run(self):
        self.reset_viz()
        self.running = True

        path, expanded, cost, ms = run_search(
            self.algo.get(),
            self.heur.get(),
            self.grid,
            self.rows,
            self.cols,
            self.start,
            self.goal
        )

        self.nodes_var.set(str(len(expanded)))
        self.cost_var.set(str(cost))
        self.time_var.set(str(ms))

        self.visited_set = expanded
        self.path_set = set(path)
        self.path_list = path

        self.redraw()

        if path:
            self.agent_idx = 0
            self.next_step(path)
        else:
            self.running = False
            tk.messagebox.showinfo("No Path", "No path found to the goal.")

    def next_step(self, path):
        if not self.running or self.agent_idx >= len(path):
            self.running = False
            return

        self.agent_pos = path[self.agent_idx]
        self.agent_idx = self.agent_idx + 1

        if self.dynamic.get():
            self.maybe_add_obstacle(path)

        self.redraw()
        self.root.after(ANIM_MS, lambda: self.next_step(path))

    def maybe_add_obstacle(self, path):
        if random.random() >= SPAWN_CHANCE:
            return

        r = random.randint(0, self.rows - 1)
        c = random.randint(0, self.cols - 1)

        is_empty = self.grid[r][c] == EMPTY_CELL
        is_not_start_or_goal = (r, c) != self.start and (r, c) != self.goal
        is_not_agent = (r, c) != self.agent_pos

        if not is_empty or not is_not_start_or_goal or not is_not_agent:
            return

        self.grid[r][c] = WALL_CELL

        remaining = set(path[self.agent_idx:])

        if (r, c) in remaining:
            self.replan()

    def replan(self):
        if self.agent_pos is None:
            return

        path, expanded, cost, _ = run_search(
            self.algo.get(),
            self.heur.get(),
            self.grid,
            self.rows,
            self.cols,
            self.agent_pos,
            self.goal
        )

        if not path:
            self.running = False
            return

        travelled = self.path_list[:self.agent_idx]
        full_path = travelled + path

        self.path_list = full_path
        self.path_set = set(full_path)
        self.visited_set = self.visited_set | expanded

        self.nodes_var.set(str(len(self.visited_set)))
        self.cost_var.set(str(len(full_path) - 1))


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    dialog = GridSizeDialog(root)

    if dialog.result is not None:
        rows = dialog.result[0]
        cols = dialog.result[1]
    else:
        rows = DEFAULT_ROWS
        cols = DEFAULT_COLS

    root.deiconify()
    App(root, rows, cols)
    root.mainloop()
