from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import codecs
import csv
import distutils.util
import textacy

def main():
    """
    Normalizes the contents of a text file using a simple naive normalization scheme.
    Designed for English
    """

    # Parse command line args
    parser = argparse.ArgumentParser(description='Normalize text in the given columns')

    parser.add_argument('-i', '--input', required=True,
        help='Path to input file')
    parser.add_argument('-c', '--cols', required=True, type=str, default=0, 
        help='Comma separated list of columns indices to normalize')
    parser.add_argument('-d', '--delimiter', required=True, default='\t', 
        help='Column delimiter between row and label')
    parser.add_argument('-header', '--hasheader', required=False, type=distutils.util.strtobool,
        default='False', help='File has header row?')
    parser.add_argument('-o', '--output', required=True, help='Path to output file')

    # Text preprocess args
    parser.add_argument('--fix_unicode', required=False, type=distutils.util.strtobool,
        default='False', help='if True, fix “broken” unicode such as mojibake and garbled HTML entities')
    parser.add_argument('--lowercase', required=False, type=distutils.util.strtobool,
        default='False', help='if True, all text is lower-cased')
    parser.add_argument('--transliterate', required=False, type=distutils.util.strtobool,
        default='False', help='if True, convert non-ascii characters into their closest ascii equivalents')
    parser.add_argument('--no_urls', required=False, type=distutils.util.strtobool,
        default='False', help='if True, replace all URL strings with ‘URL‘')
    parser.add_argument('--no_emails', required=False, type=distutils.util.strtobool,
        default='False', help='if True, replace all email strings with ‘EMAIL‘')
    parser.add_argument('--no_phone_numbers', required=False, type=distutils.util.strtobool,
        default='False', help='if True, replace all phone number strings with ‘PHONE‘')
    parser.add_argument('--no_numbers', required=False, type=distutils.util.strtobool,
        default='False', help='if True, replace all number-like strings with ‘NUMBER‘')
    parser.add_argument('--no_currency_symbols', required=False, type=distutils.util.strtobool,
        default='False', help='if True, replace all currency symbols with their standard 3-letter abbreviations')
    parser.add_argument('--no_punct', required=False, type=distutils.util.strtobool,
        default='False', help='if True, remove all punctuation (replace with empty string)')
    parser.add_argument('--no_contractions', required=False, type=distutils.util.strtobool,
        default='False', help='if True, replace English contractions with their unshortened forms')
    parser.add_argument('--no_accents', required=False, type=distutils.util.strtobool,
        default='False', help='if True, replace all accented characters with unaccented versions; NB: if transliterate is True, this option is redundant')
    parser.add_argument('--normalize_whitespace', required=False, type=distutils.util.strtobool,
        default='False', help='if True, Fix unicode text that’s “broken” using ftfy; this includes mojibake, HTML entities and other code cruft, and non-standard forms for display purposes')

    args = parser.parse_args()
    # Unescape the delimiter
    args.delimiter = codecs.decode(args.delimiter, "unicode_escape")
    # Parse cols into list of ints
    args.cols = [int(x) for x in args.cols.split(',')]

    # Convert args to dict
    vargs = vars(args)

    print("\nArguments:")
    for arg in vargs:
        print("{}={}".format(arg, getattr(args, arg)))

    # Read the input file
    with open(args.input, 'r', encoding='iso-8859-1') as inputfile:
        with open(args.output, 'w') as outputfile:
            
            reader = csv.reader(inputfile, delimiter=args.delimiter)
            writer = csv.writer(outputfile, delimiter=args.delimiter)

            # If has header, write it unprocessed
            if args.hasheader:
                headers = next(reader, None)
                if headers:
                    writer.writerow(headers)

            print("\nProcessing input")
            i = 0
            for row in reader:
                row = [textacy.preprocess_text(col,
                            fix_unicode=args.fix_unicode,
                            lowercase=args.lowercase,
                            transliterate=args.transliterate,
                            no_urls=args.no_urls,
                            no_emails=args.no_emails,
                            no_phone_numbers=args.no_phone_numbers,
                            no_numbers=args.no_numbers,
                            no_currency_symbols=args.no_currency_symbols,
                            no_punct=args.no_punct,
                            no_contractions=args.no_contractions,
                            no_accents=args.no_accents)
                        if idx in args.cols else col for idx, col in enumerate(row)]
                if args.normalize_whitespace:
                    row = [textacy.preprocess.normalize_whitespace(col)
                            if idx in args.cols else col for idx, col in enumerate(row)]

                if i<5:
                    print(row)
                    print(textacy.preprocess.preprocess_text(row[0],
                            fix_unicode=args.fix_unicode,
                            lowercase=args.lowercase,
                            transliterate=args.transliterate,
                            no_urls=args.no_urls,
                            no_emails=args.no_emails,
                            no_phone_numbers=args.no_phone_numbers,
                            no_numbers=args.no_numbers,
                            no_currency_symbols=args.no_currency_symbols,
                            no_punct=args.no_punct,
                            no_contractions=args.no_contractions,
                            no_accents=args.no_accents)
                    )
                    i+=1
                writer.writerow(row)

    print("\nDone. Bye!")

if __name__ == '__main__':
    main()
