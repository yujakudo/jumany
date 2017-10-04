"""
Interactive
"""
import sys
import unicodedata
import argparse
import jumany

def column_print(data: []):
    """ Print data in columns   """
    columns = [12, 12, 12, 10, 10, 12, 10]
    for (show, col_width) in zip(data, columns):
        width = sum([
            2 if unicodedata.east_asian_width(x) in "FWA" else 1 for x in show
        ])
        while width > col_width:
            width -= 2 if unicodedata.east_asian_width(show[len(show)-1]) in "FWA" else 1
            show = show[:len(show)-1]
        if width < col_width:
            show += (' ' * (col_width - width))
        sys.stdout.write(show)
    sys.stdout.write("\n")

parser = argparse.ArgumentParser(
    description="""Results are shown in columns by default.
    Specify delimiter not to show in columns.
    Type 'exit' in half-width charactors to exit."""
)
parser.add_argument(
    '-d', dest='delimiter', nargs='?', const=' ',
    help='delimiter of parameters. default is a space'
)
parser.add_argument(
    '-r', dest='rcf', help='path to resource file'
)
args = parser.parse_args()

if jumany.open_lib(args.rcf) is False:
    print(jumany.get_error_msg())
    sys.exit(0)

while True:
    line = sys.stdin.readline()
    if line.strip() == "exit":
        break
    Mrphs = jumany.analyze(line, True)
    if Mrphs is None:
        print(jumany.get_error_msg())
        continue
    for (Midasi1, Yomi, Midasi2, Hinsi, Bunrui, Katuyou1, Katuyou2) in Mrphs:
        mrph = [
            Midasi1, Yomi, Midasi2, jumany.get_hinsi(Hinsi),
            jumany.get_bunrui(Hinsi, Bunrui), jumany.get_katuyou1(Katuyou1),
            jumany.get_katuyou2(Katuyou1, Katuyou2)
        ]
        if args.delimiter is None:
            column_print(mrph)
        else:
            sys.stdout.write(args.delimiter.join(mrph)+"\n")
    print("EOS")
