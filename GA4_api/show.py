from tabulate import tabulate

data = ["Alice", "Bob", "Charlie"]

print(tabulate([data], tablefmt="grid"))


# "plain": Outputs a simple plain-text table with no grid lines.
# "simple": Outputs a simple table with grid lines separating the rows and columns.
# "grid": Outputs a table with thicker grid lines separating the rows and columns.
# "pipe": Outputs a table using pipe characters to separate the rows and columns.
# "orgtbl": Outputs a table in the format used by the Emacs Org mode.
# "rst": Outputs a table in reStructuredText format.
# "mediawiki": Outputs a table in the format used by MediaWiki.