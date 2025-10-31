import sys
from BST import BST
from search_engine import search_loop

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py words.txt")
        print("  python main.py --url https://example.com/words.txt")
        sys.exit(1)

    if sys.argv[1] == "--url":
        if len(sys.argv) < 3:
            print("Please provide a URL after --url.")
            sys.exit(1)
        bst = BST(sys.argv[2], url=True)
    else:
        bst = BST(sys.argv[1], file=True)

    search_loop(bst)

if __name__ == "__main__":
    main()
