from Node import Node
import urllib.request

class BST:
    def __init__(self, source: str, **kwargs):
        url_mode = kwargs.get("url", False)
        file_mode = kwargs.get("file", False)

        if url_mode and file_mode:
            raise ValueError("Choose either url=True or file=True, not both.")
        if not (url_mode or file_mode):
            raise ValueError("You must specify url=True or file=True.")

        # --- Load words ---
        if url_mode:
            with urllib.request.urlopen(source) as f:
                data = f.read().decode("utf-8")
                words = data.splitlines()
        else:
            with open(source, encoding="utf-8") as f:
                words = [line.strip() for line in f]

        # --- Clean and prepare ---
        words = sorted({w.lower().strip() for w in words if w.strip()})

        # --- Build balanced BST ---
        self.root = self._build_tree(words, 0, len(words) - 1)

        # list for storing results
        self.results = []

    # Helper: build balanced tree recursively
    def _build_tree(self, arr, start, end):
        if start > end:
            return None
        mid = (start + end) // 2
        node = Node(arr[mid])
        node.left = self._build_tree(arr, start, mid - 1)
        node.right = self._build_tree(arr, mid + 1, end)
        return node

    # Public wrapper
    def autocomplete(self, prefix: str):
        self.results = []
        prefix = prefix.lower()
        self._collect(self.root, prefix)
        return self.results

    # Private recursive collector
    def _collect(self, node, prefix):
        if not node:
            return
        if node.word < prefix:
            self._collect(node.right, prefix)
        elif node.word.startswith(prefix):
            self._collect(node.left, prefix)
            self.results.append(node.word)
            self._collect(node.right, prefix)
        else:
            self._collect(node.left, prefix)
